FROM python:3.12-slim
WORKDIR /app
COPY product-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY product-service/app ./app
COPY common ./common
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8002"]
