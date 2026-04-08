# Model Accuracy Metrics Guide

This project now includes comprehensive model performance metrics: **Accuracy**, **Precision**, **Recall**, and **F1 Score**. These metrics are automatically calculated during model training and displayed during prediction.

## 📊 Metrics Explained

### **Accuracy**
- **Definition**: Percentage of correct predictions out of total predictions
- **Formula**: `(TP + TN) / (TP + TN + FP + FN)`
- **When to use**: Good overall metric when classes are balanced
- **Range**: 0.0 to 1.0 (0% to 100%)

### **Precision** 
- **Definition**: Of all positive predictions, how many were actually correct?
- **Formula**: `TP / (TP + FP)`
- **When to use**: Important when false positives are costly (e.g., fraud flagging legitimate users)
- **Range**: 0.0 to 1.0
- **Example**: If model predicts 100 fraud cases, precision tells what % were actually fraud

### **Recall** (Sensitivity / True Positive Rate)
- **Definition**: Of all actual positives, how many did the model catch?
- **Formula**: `TP / (TP + FN)`
- **When to use**: Important when false negatives are costly (e.g., missing actual fraud)
- **Range**: 0.0 to 1.0
- **Example**: If there are 100 actual fraud cases, recall tells what % the model caught

### **F1 Score** (Harmonic Mean)
- **Definition**: Balanced combination of Precision and Recall
- **Formula**: `2 * (Precision × Recall) / (Precision + Recall)`
- **When to use**: When you need a single metric balancing both precision and recall
- **Range**: 0.0 to 1.0
- **Interpretation**: Higher is better

---

## 🔧 Where Metrics Are Calculated

### **Fraud Detection Model** (`train_fraud.py`)
- **Model**: Random Forest Classifier
- **Features**: 4 features (session_duration, clicks, events_count, click_rate)
- **Target**: is_bot (binary classification)
- **Output**: `models/fraud_metrics.json`
- **Test Split**: 80% train, 20% test

### **Conversion Prediction Model** (`train_conversion.py`)
- **Model**: Logistic Regression
- **Features**: 14 features (behavioral, temporal, user-level)
- **Target**: converted (binary classification)
- **Output**: `models/conversion_metrics.json`
- **Test Split**: 80% train, 20% test

---

## 📁 Metrics Files

### `models/fraud_metrics.json`
```json
{
  "model": "Fraud Detection (Random Forest)",
  "accuracy": 0.9234,
  "precision": 0.8945,
  "recall": 0.8712,
  "f1_score": 0.8827,
  "confusion_matrix": {
    "true_positives": 435,
    "true_negatives": 1765,
    "false_positives": 52,
    "false_negatives": 53
  },
  "training_samples": 8000,
  "test_samples": 2000
}
```

### `models/conversion_metrics.json`
```json
{
  "model": "Conversion Prediction (Logistic Regression)",
  "accuracy": 0.8967,
  "precision": 0.8654,
  "recall": 0.8234,
  "f1_score": 0.8440,
  "confusion_matrix": {
    "true_positives": 412,
    "true_negatives": 1698,
    "false_positives": 67,
    "false_negatives": 86
  },
  "training_samples": 8000,
  "test_samples": 2000
}
```

---

## 🚀 Running Models with Metrics

### Train Models (with metrics calculation)
```bash
# Train fraud detection model
python src/train_fraud.py

# Train conversion prediction model
python src/train_conversion.py
```

**Output Example**:
```
==================================================
✅ Fraud Model Training Complete
==================================================
Accuracy:  0.9234
Precision: 0.8945
Recall:    0.8712
F1 Score:  0.8827
==================================================
True Positives:  435
True Negatives:  1765
False Positives: 52
False Negatives: 53
==================================================
📊 Metrics saved to fraud_metrics.json
```

### Run Predictions (with metrics display)
```bash
# Get fraud detection predictions
python src/run_fraud.py

# Get conversion predictions with metrics
python src/test_conversion.py
```

**Output Example**:
```
======================================================================
📊 MODEL PERFORMANCE METRICS
======================================================================

Model: Fraud Detection (Random Forest)
Training Samples: 8000 | Test Samples: 2000

Accuracy Metrics:
  • Accuracy:  0.9234 (92.34%)
  • Precision: 0.8945
  • Recall:    0.8712
  • F1 Score:  0.8827

Confusion Matrix:
  • True Positives:  435
  • True Negatives:  1765
  • False Positives: 52
  • False Negatives: 53
======================================================================
```

---

## 📊 Reports with Metrics

When generating comprehensive reports:
```bash
python src/reports.py
```

Both `report_fraud_bot.json` and `report_conversion_drop.json` now include:
```json
"model_performance": {
  "accuracy": 0.9234,
  "precision": 0.8945,
  "recall": 0.8712,
  "f1_score": 0.8827,
  "confusion_matrix": {...}
}
```

---

## 🎯 Interpretation Guide

### Model Performance Assessment

| F1 Score | Assessment | Action |
|----------|-----------|--------|
| 0.90 - 1.0 | Excellent | ✅ Ready for production |
| 0.80 - 0.89 | Good | ✅ Good performance |
| 0.70 - 0.79 | Fair | ⚠️  Monitor performance |
| < 0.70 | Poor | ❌ Retrain or improve features |

### Precision vs Recall Trade-off

**High Precision, Low Recall**:
- Few false positives
- May miss actual cases
- Use when: False alarms are costly

**Low Precision, High Recall**:
- Catches most cases
- Some false positives
- Use when: Missing cases is costly

**Balanced (High F1)**:
- Good balance between both
- Use when: Both errors are equally important

---

## 🔄 Confusion Matrix Interpretation

```
                 Predicted Positive    Predicted Negative
Actual Positive  True Positive (TP)    False Negative (FN)
Actual Negative  False Positive (FP)   True Negative (TN)
```

- **TP**: Correctly identified fraud/conversion
- **TN**: Correctly identified legitimate/non-conversion  
- **FP**: False alarm (legitimate flagged as fraud)
- **FN**: Missed case (fraud not detected)

---

## 📈 Improving Model Metrics

### Strategies to Improve Accuracy
1. ✅ Add more relevant features
2. ✅ Clean and preprocess data
3. ✅ Tune hyperparameters
4. ✅ Use ensemble methods
5. ✅ Collect more training data

### Strategies to Improve Precision
1. ✅ Increase decision threshold
2. ✅ Focus on feature quality
3. ✅ Use cost-sensitive learning
4. ✅ Handle class imbalance

### Strategies to Improve Recall
1. ✅ Decrease decision threshold
2. ✅ Adjust class weights
3. ✅ Try different algorithms
4. ✅ Engineer better features

---

## 📝 Next Steps

1. ✅ **Review metrics** in JSON files after training
2. ✅ **Monitor metrics** across different data samples
3. ✅ **Adjust thresholds** based on business needs
4. ✅ **Retrain periodically** with new data
5. ✅ **Set up alerts** if metrics degrade

