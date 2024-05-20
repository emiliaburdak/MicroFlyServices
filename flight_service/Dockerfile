FROM python:3.9

WORKDIR /flight_service

COPY requirements.txt /flight_service/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /flight_service

CMD ["uvicorn", "flight_service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
