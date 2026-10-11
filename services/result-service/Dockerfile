FROM python:3.12-slim
WORKDIR /app
COPY services/result-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/result-service ./services/result-service
WORKDIR /app/services/result-service
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
