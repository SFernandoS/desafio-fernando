# Use the official Python image as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

RUN opentelemetry-bootstrap -a install

ENV OTEL_SERVICE_NAME=dice
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
ENV OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

ENV OTEL_EXPORTER_OTLP_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
ENV OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=grpc


# Command to run the FastAPI application with uvicorn
CMD ["opentelemetry-instrument", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
