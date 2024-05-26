FROM python:3.9

WORKDIR /user_service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /user_service

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
