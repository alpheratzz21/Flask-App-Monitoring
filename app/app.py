from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# counter metric using label endpoint
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["endpoint"]
)

# histogram latency
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds", "Request latency", ["endpoint"]

)

@app.route("/")
def hello_world():
    with REQUEST_LATENCY.labels(endpoint="/").time():
        REQUEST_COUNT.labels(endpoint="/").inc()
        return {"message": "Hello, World from Flask!"}

@app.route("/health")
def health():
    with REQUEST_LATENCY.labels(endpoint="/health").time():
        REQUEST_COUNT.labels(endpoint="/health").inc()
        return {"status": "ok"}

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
