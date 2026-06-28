# 🚗 Car Price Prediction API

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render)
![XGBoost](https://img.shields.io/badge/Model-XGBoost-FF6600)

A production-ready machine learning API that predicts used car prices in the Indian market. Built with FastAPI, secured with JWT authentication, cached with Redis, monitored with Prometheus & Grafana, and deployed on Render.

---

## 📌 Features

- 🔐 JWT-based authentication with API key protection
- 🤖 XGBoost ML model for accurate price prediction
- ⚡ Redis caching for repeated predictions
- 📊 Prometheus metrics + Grafana dashboard monitoring
- 🐳 Fully dockerized with Docker Compose
- 🌐 Streamlit UI for easy interaction
- ☁️ Deployed on Render

---

## 🏗️ Project Structure

```
Capstone-Project/
├── app/
│   ├── api/
│   │   ├── route_auth.py          # Login endpoint
│   │   └── route_predict.py       # Prediction endpoint
│   ├── cache/
│   │   └── redis_cache.py         # Redis caching logic
│   ├── core/
│   │   ├── config.py              # App settings & env vars
│   │   ├── dependencies.py        # API key & JWT dependencies
│   │   ├── exceptions.py          # Custom exception handlers
│   │   └── security.py            # JWT token logic
│   ├── middleware/
│   │   └── logging_middleware.py  # Request logging
│   ├── models/
│   │   ├── xgb_model.pkl          # Trained XGBoost model
│   │   └── preprocessor.pkl       # Data preprocessor
│   ├── services/
│   │   └── model_service.py       # Prediction logic
│   └── main.py                    # FastAPI app entry point
├── data/
│   └── car.csv                    # Training dataset
├── notebook/
│   └── Model-Generation.ipynb     # Model training notebook
├── Dockerfile                     # API Docker config
├── Dockerfile.ui                  # UI Docker config
├── docker-compose.yml             # Multi-container setup
├── render.yaml                    # Render deployment config
├── prometheus.yml                 # Prometheus config
├── ui.py                          # Streamlit frontend
├── requirements.txt               # API dependencies
└── requirements.ui.txt            # UI dependencies
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| ML Model | XGBoost |
| Authentication | JWT + API Key |
| Caching | Redis |
| Monitoring | Prometheus + Grafana |
| Frontend | Streamlit |
| Containerization | Docker + Docker Compose |
| Deployment | Render |

---

## 🚀 Run Locally with Docker

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/parth-kachhadiya/FastAPI-Project-1
cd FastAPI-Project-1

# 2. Build and start all services
docker-compose up --build

# 3. Access the services
```

| Service | URL |
|---|---|
| API Docs (Swagger) | http://localhost:8000/docs |
| Streamlit UI | http://localhost:8501 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

## 🔐 Authentication

All prediction requests require authentication. First login to get a JWT token, then use it for predictions.

### Step 1 — Login

**POST** `/auth`

Headers:
```
api_key: admin
```

Body:
```json
{
  "username": "admin",
  "password": "admin"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 📡 API Endpoints

### Predict Car Price

**POST** `/predict`

Headers:
```
token: <your_jwt_token>
api-key: admin
```

Request Body:
```json
{
  "brand": "Maruti",
  "model": "Swift",
  "vehicle_age": 3,
  "km_driven": 30000,
  "mileage": 21.4,
  "engine": 1197,
  "max_power": 82.0,
  "seats": 5,
  "transmission_type": "Manual",
  "seller_type": "Dealer",
  "fuel_type": "Petrol"
}
```

Response:
```json
{
  "predicted_price": "4,85,320.00"
}
```

> 💡 Use `/docs` (Swagger UI) to explore and test all endpoints interactively.

---

## 📊 Monitoring

### Prometheus
Metrics are auto-collected via `prometheus-fastapi-instrumentator` and available at:
```
http://localhost:9090
```

### Grafana
Dashboard available at:
```
http://localhost:3000
```
Default Grafana credentials: `admin / admin`

Add Prometheus as a data source:
- URL: `http://prometheus:9090`
- Then create panels to visualize request count, latency, and error rates.

---

## ☁️ Deployment on Render

This project uses `render.yaml` for Blueprint deployment.

### Steps

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → **Blueprint**
3. Connect your GitHub repository
4. Render auto-detects `render.yaml` and deploys:
   - FastAPI API service
   - Streamlit UI service
   - Redis instance

### Live URLs (after deploy)
| Service | URL |
|---|---|
| API | `https://fastapi-car-price-api.onrender.com` |
| API Docs | `https://fastapi-car-price-api.onrender.com/docs` |
| UI | `https://car-price-ui.onrender.com` |

> ⚠️ **Free tier note:** Services sleep after 15 minutes of inactivity. First request after sleep may take 30–60 seconds to respond.

---

## 🧠 ML Model

- **Algorithm:** XGBoost Regressor
- **Target:** Log-transformed selling price (converted back with `np.expm1`)
- **Features:** Brand, Model, Vehicle Age, KM Driven, Mileage, Engine, Max Power, Seats, Transmission, Seller Type, Fuel Type
- **Preprocessing:** Handled via a `scikit-learn` pipeline saved as `preprocessor.pkl`
- Training details available in `notebook/Model-Generation.ipynb`

---

## 👤 Author

**Parth Kachhadiya**

[![GitHub](https://img.shields.io/badge/GitHub-parth--kachhadiya-181717?logo=github)](https://github.com/parth-kachhadiya/FastAPI-Project-1)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).