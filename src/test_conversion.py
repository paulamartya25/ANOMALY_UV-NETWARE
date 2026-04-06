import pandas as pd
import joblib
import json

# ==============================
# 1. LOAD MODEL & SCALER
# ==============================
model = joblib.load("../models/conversion_model.pkl")
scaler = joblib.load("../models/conversion_scaler.pkl")

# ==============================
# 2. LOAD DATASET (HISTORICAL)
# ==============================
full_df = pd.read_csv("../data/analytics_dataset_10k.csv")
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

# ==============================
# 3. LOAD INPUT JSON
# ==============================
with open("../data/input.json", "r") as f:
    input_data = json.load(f)

input_df = pd.DataFrame(input_data)
input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])

# Mark new rows
input_df["is_new"] = True
full_df["is_new"] = False

# ==============================
# 4. COMBINE DATA
# ==============================
df = pd.concat([full_df, input_df], ignore_index=True)

# ==============================
# 5. FEATURE ENGINEERING (SAME AS TRAINING)
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

# ==============================
# 6. SELECT FEATURES
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

# ==============================
# 7. SCALE + PREDICT
# ==============================
X_scaled = scaler.transform(X)

# Get conversion probability (0 = not convert, 1 = will convert)
df['conversion_prediction'] = model.predict(X_scaled)
df['conversion_probability'] = model.predict_proba(X_scaled)[:, 1]  # Probability of conversion

# ==============================
# 8. EXTRACT ONLY INPUT RESULTS
# ==============================
result_df = df[df["is_new"] == True]

# ==============================
# 9. CREATE OUTPUT JSON
# ==============================
output = []

for _, row in result_df.iterrows():
    output.append({
        "session_id": row["session_id"],
        "visitor_id": row["visitor_id"],
        "will_convert": bool(row["conversion_prediction"]),
        "conversion_probability": round(float(row["conversion_probability"]), 4),
        "conversion_likelihood": "HIGH" if row["conversion_probability"] > 0.7 else ("MEDIUM" if row["conversion_probability"] > 0.4 else "LOW")
    })

# Save output
with open("../models/conversion_output.json", "w") as f:
    json.dump(output, f, indent=4)

# ==============================
# 10. PRINT RESULTS
# ==============================
print("\n" + "="*70)
print("🔮 CONVERSION PREDICTION RESULTS".center(70))
print("="*70)

for item in output:
    print(f"\nSession: {item['session_id']} | Visitor: {item['visitor_id']}")
    print(f"  • Will Convert: {item['will_convert']}")
    print(f"  • Probability: {item['conversion_probability']*100:.2f}%")
    print(f"  • Likelihood: {item['conversion_likelihood']}")

print("\n" + "="*70)
print(f"Total Sessions Analyzed: {len(output)}")
print(f"Predicted to Convert: {sum([1 for x in output if x['will_convert']])}")
print(f"Average Conversion Probability: {sum([x['conversion_probability'] for x in output])/len(output)*100:.2f}%")
print("="*70 + "\n")
