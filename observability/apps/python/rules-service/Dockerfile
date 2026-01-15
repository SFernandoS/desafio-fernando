FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && opentelemetry-bootstrap -a install

COPY . .

ENV OTEL_SERVICE_NAME=rules-service
ENV OTEL_TRACES_EXPORTER=otlp
ENV OTEL_METRICS_EXPORTER=otlp
ENV OTEL_LOGS_EXPORTER=otlp
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
ENV OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc

EXPOSE 8003

ENTRYPOINT ["opentelemetry-instrument"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
