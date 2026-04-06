import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("../data/analytics_dataset_10k.csv")

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
# TRAIN MODEL
# ==============================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ==============================
# SAVE MODEL
# ==============================
joblib.dump(model, "../models/fraud_model.pkl")

print("✅ Fraud model trained & saved")