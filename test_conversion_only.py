#!/usr/bin/env python3
"""
TEST CONVERSION MODEL ONLY
Run this to test ONLY the Conversion Prediction model
Does NOT retrain - uses saved model
"""

import pandas as pd
import joblib
import json

# ==============================
# 1. LOAD SAVED MODEL & SCALER (NO TRAINING)
# ==============================
print("\n[LOADING] Conversion Prediction Model...\n")
model = joblib.load("models/conversion_model.pkl")
scaler = joblib.load("models/conversion_scaler.pkl")

# ==============================
# 2. LOAD DATA FOR PREDICTIONS
# ==============================
full_df = pd.read_csv("data/analytics_dataset_10k.csv")
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

with open("data/input.json", "r") as f:
    input_data = json.load(f)

input_df = pd.DataFrame(input_data)
input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])

# Mark rows
input_df["is_new"] = True
full_df["is_new"] = False

# ==============================
# 3. COMBINE DATA
# ==============================
df = pd.concat([full_df, input_df], ignore_index=True)

# ==============================
# 4. FEATURE ENGINEERING (SAME AS TRAINING)
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

df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek

df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)
df['pages_per_session'] = df['pages_viewed'] / (df['session_duration'] + 1)

# ==============================
# 5. SELECT FEATURES
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
# 6. SCALE + PREDICT
# ==============================
X_scaled = scaler.transform(X)

df['conversion_prediction'] = model.predict(X_scaled)
df['conversion_probability'] = model.predict_proba(X_scaled)[:, 1]

# ==============================
# 7. EXTRACT RESULTS
# ==============================
result_df = df[df["is_new"] == True]

output = []
for _, row in result_df.iterrows():
    output.append({
        "session_id": row["session_id"],
        "visitor_id": row["visitor_id"],
        "will_convert": bool(row["conversion_prediction"]),
        "conversion_probability": round(float(row["conversion_probability"]), 4),
        "conversion_likelihood": "HIGH" if row["conversion_probability"] > 0.7 else ("MEDIUM" if row["conversion_probability"] > 0.4 else "LOW")
    })

with open("models/conversion_output.json", "w") as f:
    json.dump(output, f, indent=4)

# ==============================
# 8. LOAD & DISPLAY METRICS
# ==============================
try:
    with open("models/conversion_metrics.json", "r") as f:
        metrics = json.load(f)
    
    print("\n" + "="*80)
    print("[MODEL PERFORMANCE METRICS]".center(80))
    print("="*80)
    print(f"\nModel: {metrics['model']}")
    print(f"Training Samples: {metrics['training_samples']} | Test Samples: {metrics['test_samples']}")
    print("\n[ACCURACY METRICS]")
    print(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1 Score:  {metrics['f1_score']:.4f}")
    
    cm = metrics['confusion_matrix']
    print("\n[CONFUSION MATRIX]")
    print(f"  True Positives:  {cm['true_positives']}")
    print(f"  True Negatives:  {cm['true_negatives']}")
    print(f"  False Positives: {cm['false_positives']}")
    print(f"  False Negatives: {cm['false_negatives']}")
    print("="*80)
except Exception as e:
    print(f"\n[WARNING] Could not load metrics: {e}")

# ==============================
# 9. PRINT PREDICTIONS
# ==============================
print("\n" + "="*80)
print("[CONVERSION PREDICTION RESULTS]".center(80))
print("="*80)

for item in output:
    print(f"\nSession: {item['session_id']} | Visitor: {item['visitor_id']}")
    print(f"  Will Convert: {item['will_convert']}")
    print(f"  Probability: {item['conversion_probability']*100:.2f}%")
    print(f"  Likelihood: {item['conversion_likelihood']}")

print("\n" + "="*80)
print(f"Total Sessions: {len(output)}")
print(f"Predicted to Convert: {sum([1 for x in output if x['will_convert']])}")
print(f"Average Conversion Probability: {sum([x['conversion_probability'] for x in output])/len(output)*100:.2f}%")
print("="*80 + "\n")
