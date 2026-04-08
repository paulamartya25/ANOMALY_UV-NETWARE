import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score, accuracy_score, confusion_matrix
import json

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data/analytics_dataset_10k.csv")

# ==============================
# FEATURE ENGINEERING
# ==============================
df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)

# ==============================
# FEATURES + TARGET
# ==============================
features = ["session_duration", "clicks", "events_count", "click_rate"]

X = df[features]
y = df["is_bot"]   # target

# ==============================
# TRAIN/TEST SPLIT
# ==============================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==============================
# TRAIN MODEL
# ==============================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ==============================
# CALCULATE METRICS
# ==============================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

metrics = {
    "model": "Fraud Detection (Random Forest)",
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
# SAVE MODEL
# ==============================
joblib.dump(model, "models/fraud_model.pkl")

# ==============================
# SAVE METRICS
# ==============================
with open("models/fraud_metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

print("\n[SUCCESS] Fraud Model Training Complete")
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
print("[INFO] Metrics saved to fraud_metrics.json")