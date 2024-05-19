FROM python:3.9

WORKDIR /flight_service

COPY ./flight_service/requirements.txt /flight_service

RUN pip install --no-cache-dir -r requirements.txt

COPY ./flight_service /flight_service

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
