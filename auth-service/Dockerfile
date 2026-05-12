FROM python:3.12-slim
WORKDIR /app
COPY auth-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auth-service/app ./app
COPY auth-service/alembic.ini ./alembic.ini
COPY auth-service/alembic ./alembic
COPY common ./common
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]