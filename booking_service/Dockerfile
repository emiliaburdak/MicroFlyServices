FROM python:3.9

WORKDIR /booking_service

COPY ./booking_service/requirements.txt /booking_service

RUN pip install --no-cache-dir -r requirements.txt

COPY ./booking_service /booking_service

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
