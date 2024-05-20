FROM python:3.9

WORKDIR /gateway_service

COPY requirements.txt /gateway_service/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /gateway_service

CMD ["uvicorn", "gateway_service.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
