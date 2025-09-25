from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest
import time

app = Flask(__name__)

# counter metric for counting request
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["endpoint"])

# histogram metric for latency
REQUEST_LATENCY = Histogram("http_request_latency_seconds", "Request latency", ["endpoint"])

@app.route("/")
def hello_world():
    start = time.time()
    REQUEST_COUNT.labels(endpoint="/").inc()
    response = {"message": "Hello, World from Flask!"}
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return response

@app.route("/health")
def health():
    start = time.time()
    REQUEST_COUNT.labels(endpoint="/health").inc()
    response = {"status": "ok"}
    REQUEST_LATENCY.labels(endpoint="/health").observe(time.time() - start)
    return response

# special endpoint to expose metrics
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
