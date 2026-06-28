import streamlit as st
import requests
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_KEY      = os.getenv("API_KEY", "admin")

BRANDS = [
    "Maruti", "Hyundai", "Honda", "Mahindra", "Toyota", "Ford",
    "Volkswagen", "Renault", "BMW", "Tata", "Mercedes-Benz", "Skoda",
    "Audi", "Datsun", "Jaguar", "Land Rover", "Jeep", "Kia", "Porsche",
    "Volvo", "MG", "Mini", "Nissan", "Lexus", "Isuzu", "Bentley",
    "Maserati", "ISUZU", "Ferrari", "Mercedes-AMG", "Rolls-Royce", "Force",
]

MODELS = [
    "i20", "Swift Dzire", "Swift", "Alto", "City", "Wagon R", "Grand",
    "Innova", "Verna", "i10", "Ecosport", "Polo", "Baleno", "Amaze",
    "Ciaz", "Ertiga", "Creta", "XUV500", "KWID", "Vitara", "Scorpio",
    "Figo", "Vento", "Celerio", "Duster", "Bolero", "Fortuner", "Rapid",
    "Jazz", "3", "Tiago", "Santro", "Eeco", "E-Class", "C-Class", "5",
    "WR-V", "Safari", "A4", "Superb", "GO", "Nexon", "RediGO", "Ignis",
    "KUV", "Aspire", "A6", "Thar", "Civic", "Octavia", "Venue", "X1",
    "XF", "Rover", "Elantra", "Endeavour", "Hexa", "Compass", "Tigor",
    "7", "S-Class", "Camry", "GL-Class", "Freestyle", "Seltos", "CR-V",
    "KUV100", "X5", "Marazzo", "Q7", "X3", "Harrier", "Hector", "6",
    "Cooper", "Dzire VXI", "Yaris", "Cayenne", "XUV300", "S-Presso",
    "Triber", "GLS", "Tucson", "redi-GO", "CLS", "Kicks", "Glanza",
    "D-Max", "XL6", "XC", "Z4", "ES", "X4", "A8", "XC60", "S90",
    "Dzire ZXI", "XC90", "XE", "Carnival", "Continental", "CR", "F-PACE",
    "MUX", "X-Trail", "Panamera", "Alturas", "Wrangler", "Dzire LXI",
    "Macan", "NX", "RX", "Aura", "Ghibli", "GTC4Lusso", "Altroz", "C",
    "Ghost", "Quattroporte", "Gurkha",
]

MAE = 90000


# ── Helpers ───────────────────────────────────────────────────────────────────

def login(username: str, password: str):
    """Call /auth → returns token string or None"""
    try:
        res = requests.post(
            f"{API_BASE_URL}/auth",
            json={"username": username, "password": password},
            headers={"api_key": API_KEY},
        )
        if res.status_code == 200:
            data = res.json()
            return data.get("token")   # your route returns {'token': token}
        return None
    except Exception:
        return None


def predict(token: str, payload: dict):
    """Call /predict with token + api_key headers"""
    try:
        res = requests.post(
            f"{API_BASE_URL}/predict",
            json=payload,
            headers={
                "token"  : token,      # getCurrentUser expects 'token' header
                "api-key": API_KEY,    # getAPIKey expects 'api_key' header
            },
        )
        if res.status_code == 200:
            return res.json()
        return None
    except Exception:
        return None


def make_gauge(price: float, low: float, high: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=price,
        number={"prefix": "₹", "valueformat": ",.0f"},
        title={"text": "Estimated Price", "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, high * 1.5], "tickformat": ",.0f", "tickprefix": "₹"},
            "bar": {"color": "#2ecc71"},
            "steps": [
                {"range": [0, low],          "color": "#f0f0f0"},
                {"range": [low, price],      "color": "#d5f5e3"},
                {"range": [price, high],     "color": "#aed6f1"},
                {"range": [high, high * 1.5],"color": "#f9ebea"},
            ],
            "threshold": {
                "line": {"color": "#e74c3c", "width": 3},
                "thickness": 0.75,
                "value": price,
            },
        },
    ))
    fig.update_layout(height=350, margin=dict(t=40, b=10, l=20, r=20))
    return fig


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered",
)

if "token" not in st.session_state:
    st.session_state.token = None
if "prediction" not in st.session_state:
    st.session_state.prediction = None


# ── Login Page ────────────────────────────────────────────────────────────────

if st.session_state.token is None:
    st.title("🚗 Car Price Predictor")
    st.subheader("Login")

    with st.form("login_form"):
        username  = st.text_input("Username")
        password  = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Enter username and password.")
        else:
            with st.spinner("Authenticating..."):
                token = login(username, password)
            if token:
                st.session_state.token = token
                st.rerun()
            else:
                st.error("Invalid credentials or server unreachable.")


# ── Predict Page ──────────────────────────────────────────────────────────────

else:
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.title("🚗 Car Price Predictor")
    with col_logout:
        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.prediction = None
            st.rerun()

    st.divider()

    with st.form("predict_form"):
        st.subheader("Car Details")

        col1, col2 = st.columns(2)
        with col1:
            brand             = st.selectbox("Brand", BRANDS)
            vehicle_age       = st.number_input("Vehicle Age (years)", min_value=0, max_value=30, value=3)
            mileage           = st.number_input("Mileage (kmpl)", min_value=0.0, max_value=50.0, value=18.0, step=0.1)
            max_power         = st.number_input("Max Power (bhp)", min_value=0.0, max_value=600.0, value=82.0, step=0.1)
            transmission_type = st.selectbox("Transmission", ["Manual", "Automatic"])

        with col2:
            model             = st.selectbox("Model", MODELS)
            km_driven         = st.number_input("KM Driven", min_value=0, max_value=500000, value=30000, step=1000)
            engine            = st.number_input("Engine (cc)", min_value=500, max_value=6000, value=1200, step=100)
            seats             = st.selectbox("Seats", [2, 4, 5, 6, 7, 8, 9, 10], index=2)
            seller_type       = st.selectbox("Seller Type", ["Dealer", "Individual", "Trustmark Dealer"])

        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG", "Electric"])
        submitted = st.form_submit_button("🔍 Predict Price", use_container_width=True)

    if submitted:
        payload = {
            "brand"             : brand,
            "model"             : model,
            "vehicle_age"       : vehicle_age,
            "km_driven"         : km_driven,
            "mileage"           : mileage,
            "engine"            : engine,
            "max_power"         : max_power,
            "seats"             : seats,
            "transmission_type" : transmission_type,
            "seller_type"       : seller_type,
            "fuel_type"         : fuel_type,
        }
        with st.spinner("Predicting..."):
            result = predict(st.session_state.token, payload)

        if result:
            st.session_state.prediction = result
        else:
            st.error("Prediction failed. Check server or try again.")

    # ── Result ────────────────────────────────────────────────────────────────
    if st.session_state.prediction:
        raw       = st.session_state.prediction
        raw_price = raw if isinstance(raw, (int, float)) else raw.get("predicted_price", 0)
        price     = float(str(raw_price).replace(",", ""))   # '460,038.07' → 460038.07
        low       = max(0, price - MAE)
        high      = price + MAE

        st.divider()
        st.subheader("Prediction Result")

        st.plotly_chart(make_gauge(price, low, high), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Low Estimate",  f"₹{low:,.0f}")
        c2.metric("Predicted",     f"₹{price:,.0f}", delta="Best estimate")
        c3.metric("High Estimate", f"₹{high:,.0f}")
        st.caption(f"Confidence range ±₹{MAE:,} based on model MAE")