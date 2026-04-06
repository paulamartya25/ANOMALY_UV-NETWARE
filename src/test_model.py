import pandas as pd
import joblib
import json

# ==============================
# 1. LOAD MODEL
# ==============================
model = joblib.load("../models/isolation_forest.pkl")
scaler = joblib.load("../models/scaler.pkl")

# ==============================
# 2. LOAD DATA
# ==============================
full_df = pd.read_csv("../data/analytics_dataset_10k.csv")
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

with open("../data/input.json", "r") as f:
    input_data = json.load(f)

input_df = pd.DataFrame(input_data)
input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])

input_df["is_new"] = True
full_df["is_new"] = False

df = pd.concat([full_df, input_df], ignore_index=True)

# ==============================
# 3. FEATURE ENGINEERING
# ==============================
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

df['sessions_per_user'] = df.groupby("visitor_id")['session_id'].transform('count')
df['hour'] = df['timestamp'].dt.hour
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)

# ==============================
# 4. FEATURES
# ==============================
features = [
    "session_duration", "pages_viewed", "scroll_depth",
    "clicks", "events_count",
    "user_total_sessions", "user_avg_duration",
    "user_avg_clicks", "user_conversion_rate",
    "sessions_per_user", "click_rate",
    "events_per_click", "hour"
]

X = df[features]
X_scaled = scaler.transform(X)

# ==============================
# 5. MODEL OUTPUT
# ==============================
df['ml_anomaly'] = model.predict(X_scaled)
df['ml_anomaly'] = df['ml_anomaly'].map({1: False, -1: True})

df['anomaly_score'] = model.decision_function(X_scaled)

# ==============================
# 6. RULE-BASED FLAGS
# ==============================

# Bot detection
df['bot_flag'] = (
    (df['clicks'] > 12) &
    (df['session_duration'] < 10)
)

# Data integrity
df['data_issue'] = (
    (df['clicks'] > df['events_count']) |
    (df['session_duration'] <= 0)
)

# General rule anomaly
df['rule_flag'] = (
    (df['click_rate'] > 2) |
    (df['events_per_click'] > 5)
)

# ==============================
# 7. RISK LEVEL
# ==============================
def risk(score):
    if score < -0.2:
        return "high"
    elif score < -0.05:
        return "medium"
    else:
        return "low"

df['risk_level'] = df['anomaly_score'].apply(risk)

# ==============================
# 8. ANOMALY TYPE
# ==============================
def anomaly_type(row):
    if row["bot_flag"]:
        return "bot_activity"
    elif row["data_issue"]:
        return "data_integrity_issue"
    elif row["rule_flag"]:
        return "behavior_anomaly"
    elif row["ml_anomaly"]:
        return "ml_detected_anomaly"
    else:
        return "normal"

df['anomaly_type'] = df.apply(anomaly_type, axis=1)

# ==============================
# 9. FINAL DECISION (COMBINED)
# ==============================
df['final_anomaly'] = (
    df['ml_anomaly'] |
    df['bot_flag'] |
    df['data_issue'] |
    df['rule_flag']
)

# ==============================
# 10. OUTPUT ONLY INPUT ROWS
# ==============================
result_df = df[df["is_new"] == True]

output = []

for _, row in result_df.iterrows():
    output.append({
        "session_id": row["session_id"],
        "visitor_id": row["visitor_id"],
        "anomaly": bool(row["final_anomaly"]),
        "risk_level": row["risk_level"],
        "anomaly_score": float(row["anomaly_score"]),
        "anomaly_type": row["anomaly_type"],
        "flags": {
            "ml": bool(row["ml_anomaly"]),
            "bot": bool(row["bot_flag"]),
            "data_issue": bool(row["data_issue"]),
            "rule": bool(row["rule_flag"])
        }
    })

# ==============================
# 11. SAVE JSON
# ==============================
with open("../models/output.json", "w") as f:
    json.dump(output, f, indent=4)

print(json.dumps(output, indent=4))