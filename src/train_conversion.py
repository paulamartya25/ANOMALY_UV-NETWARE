import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score, confusion_matrix
import json

# ==============================
# 1. LOAD DATA
# ==============================
DATA_PATH = "data/analytics_dataset_10k.csv"

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
# 4. TRAIN/TEST SPLIT
# ==============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ==============================
# 5. SCALE DATA
# ==============================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Scaling Completed")

# ==============================
# 6. TRAIN MODEL
# ==============================

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

print("Model Training Completed")

# ==============================
# 7. CALCULATE METRICS
# ==============================
y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

metrics = {
    "model": "Conversion Prediction (Logistic Regression)",
    "accuracy": round(accuracy, 4),
    "precision": round(precision, 4),
    "recall": round(recall, 4),
    "f1_score": round(f1, 4),
    "confusion_matrix": {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp)
    },
    "test_samples": len(y_test),
    "training_samples": len(y_train)
}

# ==============================
# 8. SAVE MODEL + SCALER
# ==============================

joblib.dump(model, "models/conversion_model.pkl")
joblib.dump(scaler, "models/conversion_scaler.pkl")

# ==============================
# 9. SAVE METRICS
# ==============================
with open("models/conversion_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\n[SUCCESS] Conversion Model Training Complete")
print("=" * 50)
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print("=" * 50)
print(f"True Positives:  {tp}")
print(f"True Negatives:  {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print("=" * 50)
print("[INFO] Conversion model and scaler saved successfully")
print("[INFO] Metrics saved to conversion_metrics.json")