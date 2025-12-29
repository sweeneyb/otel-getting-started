# run
flask run -p 8080 --host 0.0.0.0


export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    --logs_exporter console \
    --service_name dice-server \
    flask run -p 8080 --host 0.0.0.0

export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
opentelemetry-instrument --logs_exporter otlp flask run -p 8080 --host 0.0.0.0



## Collector
podman run -p 4317:4317 \
    -v `pwd`/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    docker.io/otel/opentelemetry-collector:latest \
    --config=/etc/otel-collector-config.yaml

podman run --expose 55681 \
    --expose 4317 \
    --rm \
    -v `pwd`/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
    -v `pwd`/../secrets/service-account-key.json:/etc/otelcol-contrib/key.json \
    --env GOOGLE_APPLICATION_CREDENTIALS=/etc/otelcol-contrib/key.json \
    docker.io/otel/opentelemetry-collector-contrib:nightly-amd64 \
    --config=/etc/otel-collector-config.yaml

podman pull docker.io/otel/opentelemetry-collector-contrib:nightly-amd64