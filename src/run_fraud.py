import pandas as pd
import json
import joblib

# ==============================
# 1. LOAD DATA
# ==============================
with open("../data/input.json") as f:
    input_data = json.load(f)

input_df = pd.DataFrame(input_data)
input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])

# Load historical data for visitor stats
full_df = pd.read_csv("../data/analytics_dataset_10k.csv")
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

# Mark new rows
input_df["is_new"] = True
full_df["is_new"] = False

# ==============================
# 2. COMBINE & FEATURE ENGINEERING
# ==============================
df = pd.concat([full_df, input_df], ignore_index=True)

# Visitor-level stats (same as test_model.py)
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

# Additional features
df['sessions_per_user'] = df.groupby("visitor_id")['session_id'].transform('count')
df['hour'] = df['timestamp'].dt.hour
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)

# ==============================
# 3. LOAD MODEL & PREDICT
# ==============================
model = joblib.load("../models/fraud_model.pkl")

features = ["session_duration", "clicks", "events_count", "click_rate"]
df["fraud"] = model.predict(df[features])

# ==============================
# 4. EXTRACT & SAVE RESULTS
# ==============================
result_df = df[df["is_new"] == True]

output = []
for _, row in result_df.iterrows():
    output.append({
        "session_id": row["session_id"],
        "visitor_id": row["visitor_id"],
        "fraud": bool(row["fraud"])
    })

with open("../models/fraud_output.json", "w") as f:
    json.dump(output, f, indent=4)

print(result_df[["session_id", "visitor_id", "fraud"]])