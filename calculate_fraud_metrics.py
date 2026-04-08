import pandas as pd
import joblib
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, confusion_matrix
import json

print("\n" + "="*80)
print("[CALCULATING EXACT METRICS FOR TRAINED FRAUD MODEL]".center(80))
print("="*80)

# Load trained model
model = joblib.load("models/fraud_model.pkl")
print("\n[INFO] Loaded fraud_model.pkl")

# Load data
df = pd.read_csv("data/analytics_dataset_10k.csv")
print("[INFO] Loaded analytics_dataset_10k.csv")

# Feature engineering (same as training)
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)

# Prepare features
features = ["session_duration", "clicks", "events_count", "click_rate"]
X = df[features]
y = df["is_bot"]

print(f"[INFO] Total samples: {len(df)}")

# Make predictions
y_pred = model.predict(X)
print(f"[INFO] Predictions made on all {len(df)} samples")

# Calculate metrics
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average='weighted', zero_division=0)
recall = recall_score(y, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y, y_pred, average='weighted', zero_division=0)
tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()

print("\n" + "="*80)
print("[EXACT CALCULATED VALUES]".center(80))
print("="*80)

print(f"\n  F1 Score:   {f1:.4f}")
print(f"  Precision:  {precision:.4f}")
print(f"  Recall:     {recall:.4f}")
print(f"  Accuracy:   {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\n" + "[CONFUSION MATRIX]".center(80))
print("-" * 80)
print(f"  True Positives:  {tp}")
print(f"  True Negatives:  {tn}")
print(f"  False Positives: {fp}")
print(f"  False Negatives: {fn}")

print("\n" + "[BREAKDOWN]".center(80))
print("-" * 80)
total_fraud = tp + fn
total_legit = tn + fp
print(f"  Total Actual Fraud Cases:      {total_fraud}")
print(f"  Total Actual Legitimate Cases: {total_legit}")
print(f"  Model Caught Fraud:            {tp} out of {total_fraud} ({(tp/total_fraud)*100:.1f}%)")
print(f"  Model Flagged Legitimate:      {fp} out of {total_legit} ({(fp/total_legit)*100:.1f}%)")

print("\n" + "="*80 + "\n")
