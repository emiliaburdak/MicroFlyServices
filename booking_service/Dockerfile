FROM python:3.9

WORKDIR /booking_service

COPY requirements.txt /booking_service/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /booking_service

CMD ["uvicorn", "booking_service.app.main:app", "--host", "0.0.0.0", "--port", "8002"]
