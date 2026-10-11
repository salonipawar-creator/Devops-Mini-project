FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY services/image-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/image-service ./services/image-service
COPY config ./config
WORKDIR /app/services/image-service
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
