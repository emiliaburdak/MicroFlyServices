import json
from collections import defaultdict
from typing import List

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
import httpx

from fastapi.staticfiles import StaticFiles

from .kafka_utils import kafka_router

app = FastAPI(lifespan=kafka_router.lifespan_context)
app.include_router(kafka_router)

SERVICE_URLS = {
    "user_service": "http://user_service:8003",
    "flight_service": "http://flight_service:8001",
    "booking_service": "http://booking_service:8002"
}

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
destinations = defaultdict(int)


@app.api_route("/{service}/{path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail="Service not found!")

    url = f"{SERVICE_URLS[service]}/{path}/"
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=await request.body(),
            params=request.query_params
        )
        return resp.json()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
chart_manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.websocket("/ws/flights_chart")
async def websocket_endpoint(websocket: WebSocket):
    await chart_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        chart_manager.disconnect(websocket)


@kafka_router.subscriber("purchases-info")
async def broadcast_purchases_info(msg: str):
    await manager.broadcast(msg)


@kafka_router.subscriber("flight-info-collector")
async def collect_purchased_flights_info(flight_ids: List[int]):
    global destinations
    for flight_id in flight_ids:
        fetched_flight = await fetch_destination_data(flight_id)
        destinations[fetched_flight] += 1
        await chart_manager.broadcast(json.dumps(dict(destinations)))


async def fetch_destination_data(flight_id):
    url = f"http://127.0.0.1:8000/flight_service/flight_details?flight_id={flight_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"flight_id": flight_id})
            response.raise_for_status()
            return response.json()["destination"]
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch flight details")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail="Failed to connect to flight service")

