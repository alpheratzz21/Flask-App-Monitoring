# Flask App Monitoring on Kubernetes with Prometheus & Grafana 🚀

A mini project for **DevOps / SRE Junior** portfolio.  
This project demonstrates an end-to-end pipeline: **build a simple Flask app → containerization → deploy to Kubernetes (Minikube) → observability with Prometheus & Grafana**.

---

## 📌 Features
- **Flask App** with 2 endpoints:
  - `/` → Hello World  
  - `/health` → Health check
- **Metrics Exposure** via `/metrics` using `prometheus_client`
- **Dockerized Application** with `Dockerfile`
- **Deployment on Kubernetes (Minikube)**
- **Prometheus Integration** for scraping metrics
- **Grafana Dashboard** to monitor:
  - Total HTTP requests
  - Request rate per endpoint
  - Request distribution (Pie chart)
- **CI/CD Pipeline** with GitHub Actions - auto build & push to DockerHub on push to main
- **Error Rate Tracking** via 'http_errors_total' counter (excludes favicon noise)
- **Request Latency** via Histogram per endpoint

---

## 🏗️ Architecture

```plaintext
[Flask App] -> expose metrics (/metrics)
     |
     v
[Prometheus] -> scrape metrics
     |
     v
[Grafana] -> visualize dashboard
```

⚙️ Setup & Installation
1. Clone Repository
```
git clone https://github.com/alpheratzz21/Flask-App-Monitoring.git
cd flask-app-monitoring
```
2. Build & Push Docker Image
```
docker build -f docker/Dockerfile -t rifqiananda/flask-app:v3 .
docker push rifqiananda/flask-app:v3
```
3. Start Minikube (with Docker driver)
```
minikube start --driver=docker
```
4. Deploy App to Kubernetes
```
kubectl apply -f k8s/dev/deployment.yaml
```
5. Install Prometheus & Grafana via Helm
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus
helm install grafana grafana/grafana
```
6. Add Prometheus Additional Scrape Config

Place `prometheus-additional.yaml` in project root.

Create secret from it:
```
kubectl create secret generic additional-scrape-configs --from-file=prometheus-additional.yaml -n default
```
🔑 Access Grafana

Expose Grafana:
```
minikube service grafana --url
```

Get admin password:
```
kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
```

Default username is `admin`.

📊 Grafana Dashboard

Main metrics displayed:

Total HTTP Requests
```
sum(http_requests_total{job="flask-app"})
```

Request Rate per Endpoint
```
rate(http_requests_total{job="flask-app"}[1m])
```

Request Distribution (Pie Chart)
```
sum by (endpoint) (http_requests_total{job="flask-app"})
```
Error Rate per Endpoint

```
rate(http_errors_total{job="flask-app"}[1m])
```

📂 Project Structure
````
flask-app-monitoring/
├── app/
│   └── app.py
├── k8s/
│   └── dev/
│       └── deployment.yaml
├── Dockerfile
├── requirements.txt
├── prometheus-additional.yaml
└── README.md
````
🚀 Future Improvements

- Add Loki for log aggregation

- Add custom metrics: latency, error rate -- Done

- Setup CI/CD pipeline (GitHub Actions / Jenkins) -- Done


