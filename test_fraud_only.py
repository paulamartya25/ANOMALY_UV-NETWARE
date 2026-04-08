#!/usr/bin/env python3
"""
TEST FRAUD MODEL ONLY
Run this to test ONLY the Fraud Detection model
Does NOT retrain - uses saved model
"""

import pandas as pd
import json
import joblib

# ==============================
# 1. LOAD SAVED MODEL (NO TRAINING)
# ==============================
print("\n[LOADING] Fraud Detection Model...\n")
model = joblib.load("models/fraud_model.pkl")

# ==============================
# 2. LOAD DATA FOR PREDICTIONS
# ==============================
with open("data/input.json") as f:
    input_data = json.load(f)

input_df = pd.DataFrame(input_data)
input_df['timestamp'] = pd.to_datetime(input_df['timestamp'])

# Load historical data
full_df = pd.read_csv("data/analytics_dataset_10k.csv")
full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])

# Mark rows
input_df["is_new"] = True
full_df["is_new"] = False

# ==============================
# 3. COMBINE & FEATURE ENGINEERING
# ==============================
df = pd.concat([full_df, input_df], ignore_index=True)

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
# 4. MAKE PREDICTIONS
# ==============================
features = ["session_duration", "clicks", "events_count", "click_rate"]
df["fraud"] = model.predict(df[features])

result_df = df[df["is_new"] == True]

output = []
for _, row in result_df.iterrows():
    output.append({
        "session_id": row["session_id"],
        "visitor_id": row["visitor_id"],
        "fraud": bool(row["fraud"])
    })

with open("models/fraud_output.json", "w") as f:
    json.dump(output, f, indent=4)

# ==============================
# 5. LOAD & DISPLAY METRICS
# ==============================
try:
    with open("models/fraud_metrics.json", "r") as f:
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
# 6. PRINT PREDICTIONS
# ==============================
print("\n" + "="*80)
print("[FRAUD DETECTION PREDICTIONS]".center(80))
print("="*80)

fraud_count = sum([1 for x in output if x['fraud']])
print(f"\nTotal Sessions: {len(output)}")
print(f"Fraud Detected: {fraud_count}")
print(f"Legitimate: {len(output) - fraud_count}")
print(f"Fraud Rate: {fraud_count/len(output)*100:.2f}%\n")

for item in output:
    status = "[FRAUD]" if item['fraud'] else "[LEGITIMATE]"
    print(f"Session {item['session_id']} | Visitor {item['visitor_id']} | {status}")

print("="*80 + "\n")
