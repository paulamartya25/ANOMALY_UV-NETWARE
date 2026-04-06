import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# ==============================
# 1. LOAD DATA
# ==============================
DATA_PATH = "../data/analytics_dataset_10k.csv"

df = pd.read_csv(DATA_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])

print(f"Data Loaded: {df.shape}")

# ==============================
# 2. FEATURE ENGINEERING
# ==============================

# Visitor-level stats
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

# Time features
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek

# Behavioral features
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)
df['pages_per_session'] = df['pages_viewed'] / (df['session_duration'] + 1)

print("Feature Engineering Completed")

# ==============================
# 3. SELECT FEATURES
# ==============================

features = [
    "session_duration", "pages_viewed", "scroll_depth",
    "clicks", "events_count",
    "user_total_sessions", "user_avg_duration",
    "user_avg_clicks", "user_conversion_rate",
    "hour", "day_of_week", "click_rate",
    "events_per_click", "pages_per_session"
]

X = df[features]
y = df['converted']

# Remove rows with NaN
mask = X.notna().all(axis=1)
X = X[mask]
y = y[mask]

# ==============================
# 4. SCALE DATA
# ==============================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Scaling Completed")

# ==============================
# 5. TRAIN MODEL
# ==============================

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_scaled, y)

print("Model Training Completed")

# ==============================
# 6. SAVE MODEL + SCALER
# ==============================

joblib.dump(model, "../models/conversion_model.pkl")
joblib.dump(scaler, "../models/conversion_scaler.pkl")

print("✅ Conversion model and scaler saved successfully")