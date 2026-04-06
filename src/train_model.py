import pandas as pd
import os
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ==============================
# 1. LOAD DATA
# ==============================
DATA_PATH = "../data/analytics_dataset_10k.csv"

df = pd.read_csv(DATA_PATH)

# Convert timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(f"Data Loaded: {df.shape}")

# ==============================
# 2. FEATURE ENGINEERING
# ==============================

# Visitor-level features
visitor_stats = df.groupby("visitor_id").agg({
    "session_id": "count",
    "session_duration": "mean",
    "clicks": "mean",
    "converted": "mean"
}).rename(columns={
    "session_id": "user_total_sessions",
    "session_duration": "user_avg_duration",
    "clicks": "user_avg_clicks",
    "converted": "user_conversion_rate"
})

df = df.merge(visitor_stats, on="visitor_id", how="left")

# Sessions per user
df['sessions_per_user'] = df.groupby("visitor_id")['session_id'].transform('count')

# Time feature
df['hour'] = df['timestamp'].dt.hour

# Behavioral ratios
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)

print("Feature Engineering Completed")

# ==============================
# 3. SELECT FEATURES
# ==============================

features = [
    "session_duration",
    "pages_viewed",
    "scroll_depth",
    "clicks",
    "events_count",

    "user_total_sessions",
    "user_avg_duration",
    "user_avg_clicks",
    "user_conversion_rate",

    "sessions_per_user",
    "click_rate",
    "events_per_click",
    "hour"
]

X = df[features]

# ==============================
# 4. SCALE DATA
# ==============================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Scaling Completed")

# ==============================
# 5. TRAIN MODEL
# ==============================

model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X_scaled)

print("Model Training Completed")

# ==============================
# 6. SAVE MODEL + SCALER
# ==============================

os.makedirs("../models", exist_ok=True)

joblib.dump(model, "../models/isolation_forest.pkl")
joblib.dump(scaler, "../models/scaler.pkl")

print("Model and Scaler saved successfully in /models")