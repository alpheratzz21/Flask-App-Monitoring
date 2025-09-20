from flask import Flask
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

# counter metric for counting request
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["endpoint"])

@app.route("/")
def hello_world():
    REQUEST_COUNT.labels(endpoint="/").inc()  # every request increase counter
    return {"message": "Hello, World from Flask!"}

@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return {"status": "ok"}

# special endpoint to expose metrics
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain; charset=utf-8"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
