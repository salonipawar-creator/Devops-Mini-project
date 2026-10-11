FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*
COPY services/ai-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/ai-service ./services/ai-service
COPY config ./config
COPY ml ./ml
RUN python ml/train.py
WORKDIR /app/services/ai-service
EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
