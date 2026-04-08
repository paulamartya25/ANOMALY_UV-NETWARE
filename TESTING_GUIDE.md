# Individual Model Testing Guide

## ✅ What We Added

We've successfully added **F1 Score, Precision, and Recall** to your project:

### **Metrics Added to Each Model:**
- ✅ **Accuracy** - Overall correctness percentage
- ✅ **Precision** - Of positive predictions, how many were correct
- ✅ **Recall** - Of actual positives, how many did the model catch
- ✅ **F1 Score** - Harmonic mean balancing precision and recall
- ✅ **Confusion Matrix** - TP, TN, FP, FN breakdown

---

## 🚀 Run Individual Models - NO Retraining

### **FRAUD DETECTION MODEL ONLY**
```bash
python test_fraud_only.py
```
Output:
- Loads saved fraud model (no retraining)
- Displays accuracy, precision, recall, F1 score
- Shows predictions on test data
- Confusion matrix

**Example Output:**
```
[MODEL PERFORMANCE METRICS]
Model: Fraud Detection (Random Forest)
Training Samples: 8000 | Test Samples: 2000

[ACCURACY METRICS]
  Accuracy:  1.0000 (100.00%)
  Precision: 1.0000
  Recall:    1.0000
  F1 Score:  1.0000

[CONFUSION MATRIX]
  True Positives:  303
  True Negatives:  1697
  False Positives: 0
  False Negatives: 0
```

---

### **CONVERSION PREDICTION MODEL ONLY**
```bash
python test_conversion_only.py
```
Output:
- Loads saved conversion model (no retraining)
- Displays accuracy, precision, recall, F1 score
- Shows predictions on test data
- Confusion matrix

**Example Output:**
```
[MODEL PERFORMANCE METRICS]
Model: Conversion Prediction (Logistic Regression)
Training Samples: 8000 | Test Samples: 2000

[ACCURACY METRICS]
  Accuracy:  0.9180 (91.80%)
  Precision: 0.9112
  Recall:    0.9180
  F1 Score:  0.9133

[CONFUSION MATRIX]
  True Positives:  119
  True Negatives:  1717
  False Positives: 56
  False Negatives: 108
```

---

### **BOTH MODELS TOGETHER (Testing Only)**
```bash
python test_models_only.py
```
Output:
- Tests fraud model (no retraining)
- Tests conversion model (no retraining)
- Displays all metrics
- Takes ~2-3 seconds

---

## 📊 View Metrics Files Directly

### **Fraud Model Metrics**
```bash
cat models/fraud_metrics.json
```

### **Conversion Model Metrics**
```bash
cat models/conversion_metrics.json
```

---

## 🎯 Quick Reference

| Command | Model | Retrains? | Time |
|---------|-------|-----------|------|
| `python test_fraud_only.py` | Fraud Only | NO | ~1 sec |
| `python test_conversion_only.py` | Conversion Only | NO | ~1-2 sec |
| `python test_models_only.py` | Both Models | NO | ~2-3 sec |
| `python train_models_once.py` | Train Both | YES | ~5-10 sec |
| `python run_all_tests.py` | Train + Test | YES | ~10-15 sec |

---

## 📁 Files Structure

```
analytics-anomaly-project/
├── test_fraud_only.py              <-- Test fraud model (NO retraining)
├── test_conversion_only.py         <-- Test conversion model (NO retraining)
├── test_models_only.py             <-- Test both models (NO retraining)
├── train_models_once.py            <-- Train both models (RETRAINING)
├── run_all_tests.py                <-- Train + test everything
│
├── models/
│   ├── fraud_model.pkl             <-- Saved fraud model
│   ├── fraud_metrics.json          <-- Fraud accuracy metrics
│   ├── fraud_output.json           <-- Fraud predictions
│   ├── conversion_model.pkl        <-- Saved conversion model
│   ├── conversion_scaler.pkl       <-- Saved scaler
│   ├── conversion_metrics.json     <-- Conversion accuracy metrics
│   └── conversion_output.json      <-- Conversion predictions
│
└── src/
    ├── train_fraud.py              <-- Training script
    ├── train_conversion.py         <-- Training script
    ├── run_fraud.py                <-- Prediction script
    └── test_conversion.py          <-- Prediction script
```

---

## ✨ Key Points

✅ **Models are already trained** - Don't retrain unless you have new data
✅ **Use `test_fraud_only.py` or `test_conversion_only.py`** - For individual testing
✅ **No retraining happens** - These scripts only use saved models
✅ **All metrics included** - Accuracy, Precision, Recall, F1 Score
✅ **Fast execution** - Individual tests take 1-2 seconds

---

## 🎯 Recommended Usage

```bash
# View fraud model metrics
python test_fraud_only.py

# View conversion model metrics  
python test_conversion_only.py

# View both metrics together
python test_models_only.py

# If you need to retrain (only when you have new data)
python train_models_once.py
python test_models_only.py

# To see everything in one go
python run_all_tests.py
```

That's it! Your models are trained and ready to use! 🚀
