from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

SERVICE_URLS = {
    "user_service": "http://user_service:8003",
    "flight_service": "http://flight_service:8001",
    "booking_service": "http://booking_service:8002"
}


@app.api_route("/{service}/{path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail="Service not found")

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
