# 📊 HOW THE THREE MODELS FUNCTION

## Overview
This analytics anomaly detection system contains three machine learning models that work together to monitor, detect anomalies, and predict user behavior from website session data. Each model has a distinct purpose and uses different algorithms to analyze user sessions.

---

## MODEL 1: ANOMALY DETECTION (Isolation Forest)

### **Purpose**
Detects **behavioral anomalies** in user sessions—identifying sessions that deviate significantly from normal user behavior patterns.

### **Algorithm**
- **Type**: Unsupervised Learning (Isolation Forest)
- **Library**: scikit-learn
- **Training File**: `train_model.py`
- **Model File**: `models/isolation_forest.pkl`
- **Scaler File**: `models/scaler.pkl`

### **How It Works**
1. **Data Input**: Takes 13 behavioral features from each user session
2. **Feature Scaling**: Normalizes all features using StandardScaler (mean=0, std=1)
3. **Isolation**: Uses decision trees to isolate anomalous data points by randomly selecting features and split values
4. **Anomaly Score**: Sessions with shorter average tree path lengths are considered anomalies
5. **Classification**: Labels sessions as Normal or Anomalous

### **Features Analyzed (13 Total)**
**Session Metrics:**
- `session_duration` - How long the session lasted (seconds)
- `pages_viewed` - Number of pages visited
- `scroll_depth` - How far user scrolled (0-100%)
- `clicks` - Total clicks in session
- `events_count` - Number of tracked events

**User History (from aggregated 10k dataset):**
- `user_total_sessions` - Lifetime session count
- `user_avg_duration` - Average session length for this user
- `user_avg_clicks` - Average clicks per session
- `user_conversion_rate` - Percentage of sessions that converted

**Derived Behavioral Ratios:**
- `sessions_per_user` - Sessions per unique visitor
- `click_rate` - Clicks per second (clicks / duration)
- `events_per_click` - Event density (events / clicks)

**Temporal:**
- `hour` - Hour of day when session occurred (0-23)

### **Output**
- **Prediction**: `True` (anomalous) or `False` (normal)
- **Risk Level**: Low / Medium / High
- **Used By**: `test_model.py` to generate anomaly detection reports

### **Key Insight**
This model discovers unusual patterns without labeled data. For example:
- A user with 1,000 clicks in 5 seconds = ANOMALY
- A session lasting 3 hours with 0 interactions = ANOMALY
- A user who never converts suddenly converting 10 times = ANOMALY

---

## MODEL 2: FRAUD DETECTION (Random Forest)

### **Purpose**
Detects **bot activity and fraudulent behavior**—identifying fake or suspicious sessions that violate realistic user interaction patterns.

### **Algorithm**
- **Type**: Supervised Classification (Random Forest)
- **Library**: scikit-learn
- **Classifier**: RandomForestClassifier (100 trees)
- **Training File**: `train_fraud.py`
- **Model File**: `models/fraud_model.pkl`
- **Input Processing**: `run_fraud.py`

### **How It Works**
1. **Data Input**: Historical data labeled with `is_bot` flag (True/False)
2. **Feature Engineering**: Extracts 4 key features related to bot activity
3. **Training**: Random Forest learns patterns of fraudulent sessions
4. **Decision**: Ensemble of 100 decision trees votes on whether a session is fraudulent
5. **Probability Output**: Returns fraud likelihood (0-1)

### **Features Analyzed (4 Total)**
- `session_duration` - Session length (bot sessions often very short or very long)
- `clicks` - Click count (bots produce extreme click patterns)
- `events_count` - Event density (bots generate unrealistic event counts)
- `click_rate` - Clicks per second (bots show inhuman click rates)

### **Fraud Detection Rules**
Sessions are flagged as fraudulent based on:

| Pattern | Threshold | Fraud Points |
|---------|-----------|--------------|
| Extreme Clicks | 150+ clicks in 5 seconds | +3 |
| Extreme Events | 500+ events in 8 seconds | +3 |
| Unrealistic Scroll | 99% scroll depth in 3 seconds | +2 |
| Abnormal Pages | 50+ pages viewed in 30 seconds | +2 |
| Idle Session | 1200+ seconds with 0 clicks | +2 |

**Fraud Trigger**: Score ≥ 1 point = FRAUD ALERT

### **Output**
- **Prediction**: `True` (fraudulent) or `False` (legitimate)
- **Fraud Score**: 0-6 range
- **Fraud Types Detected**: 
  - Bot sessions (high automation)
  - Click farms
  - Event spam
  - Idle/inactive sessions
  - Unrealistic navigation
- **Used By**: `reports.py` to generate fraud detection report

### **Key Insight**
While built on labeled bot data, this model catches superhuman interaction patterns that real users cannot achieve. It prevents false conversions, skewed analytics, and identifies revenue loss from fraudulent traffic.

---

## MODEL 3: CONVERSION PREDICTION (Logistic Regression)

### **Purpose**
**Predicts the probability** that a session will result in a purchase conversion—identifying which sessions are most likely to convert.

### **Algorithm**
- **Type**: Supervised Binary Classification (Logistic Regression)
- **Library**: scikit-learn
- **Training File**: `train_conversion.py`
- **Model File**: `models/conversion_model.pkl`
- **Scaler File**: `models/conversion_scaler.pkl`
- **Testing File**: `test_conversion.py`

### **How It Works**
1. **Data Input**: Historical sessions labeled with `converted` flag (1=Yes, 0=No)
2. **Feature Engineering**: Creates 14 predictive features from user behavior
3. **Scaling**: Normalizes all features for optimal logistic regression performance
4. **Training**: Logistic regression learns the sigmoid relationship between features and conversion
5. **Probability**: Outputs conversion probability (0-1)

### **Features Analyzed (14 Total)**
**Session Engagement:**
- `session_duration` - Time spent in session
- `pages_viewed` - Number of pages viewed
- `scroll_depth` - How far user scrolled
- `clicks` - Number of interactions
- `events_count` - Tracked events

**User Historical Profile:**
- `user_total_sessions` - Lifetime visits
- `user_avg_duration` - Typical session length
- `user_avg_clicks` - Typical interaction level
- `user_conversion_rate` - Likelihood to convert (user history)

**Temporal Patterns:**
- `hour` - Hour of day (peak shopping hours?)
- `day_of_week` - Day of week (weekends vs weekdays)

**Behavioral Ratios:**
- `click_rate` - Engagement intensity (clicks/second)
- `events_per_click` - Event density per click
- `pages_per_session` - Navigation depth

### **Output**
- **Prediction**: Conversion probability (0.0 to 1.0)
- **Likelihood Categories**:
  - `LOW` (0-0.33): User unlikely to convert
  - `MEDIUM` (0.33-0.67): Moderate conversion probability
  - `HIGH` (0.67-1.0): User very likely to convert
- **Used By**: `test_conversion.py` to generate conversion prediction report

### **Key Insight**
This model learns what engaged, converting users look like. For example:
- Users who spend 15+ minutes = higher conversion probability
- First-time visitors = lower conversion probability
- Users visiting on Monday afternoon = pattern-based prediction
- High click + scroll rates = conversion indicators

---

## COMPARISON: WHEN & WHY EACH MODEL IS USED

| Aspect | Anomaly (IF) | Fraud (RF) | Conversion (LR) |
|--------|--------------|-----------|-----------------|
| **Purpose** | Find weird behavior | Find fake users | Predict buyers |
| **Type** | Unsupervised | Supervised | Supervised |
| **Algorithm** | Isolation Forest | Random Forest | Logistic Regression |
| **Input** | Unlabeled sessions | Labeled bot/real | Labeled converted/not |
| **Features** | 13 behavioral | 4 bot-focused | 14 engagement+user |
| **Output** | Anomaly flag | Fraud probability | Conversion probability |
| **Risk Level** | Low/Medium/High | 0-6 score | Low/Medium/High |
| **Use Case** | Behavior deviation | Bot detection | Revenue prediction |

---

## DATA PIPELINE: HOW MODELS WORK TOGETHER

```
┌─────────────────────────────────────────────────────────────────┐
│                   New Session (input.json)                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │ Anomaly  │ │  Fraud   │ │  Conversion  │
    │Detection │ │Detection │ │ Prediction   │
    │(IF)      │ │(RF)      │ │(LR)          │
    └──────────┘ └──────────┘ └──────────────┘
          │            │            │
          ├────────────┼────────────┤
          │    Logic   │    Rules   │    Probability
          ▼            ▼            ▼
    ┌───────────────────────────────────────┐
    │         reports.py                     │
    │  (Combines all model outputs)         │
    └───────────────────────────────────────┘
          │
          ├─ report_traffic_spike.json
          ├─ report_fraud_bot.json
          ├─ report_conversion_drop.json
          ├─ report_revenue_leakage.json
          └─ report_data_integrity.json
```

---

## TRAINING DATA

All three models are trained on:
- **Dataset**: `analytics_dataset_10k.csv` (10,000 historical sessions)
- **Features**: User behavior, engagement metrics, conversion outcomes
- **Frequency**: Models are pre-trained (not retrained per input)
- **Scaling**: Each model uses StandardScaler for feature normalization

---

## KEY DIFFERENCES IN APPROACH

### **Anomaly Detection (Isolation Forest)**
- ✓ No labels needed (unsupervised)
- ✓ Finds statistical outliers
- ✓ Detects novel/unexpected patterns
- ✗ May flag rare but legitimate behavior

### **Fraud Detection (Random Forest)**
- ✓ Uses labeled training data (supervised)
- ✓ Learns specific bot patterns
- ✓ 100 decision trees = robustness
- ✗ May miss new fraud techniques

### **Conversion Prediction (Logistic Regression)**
- ✓ Probabilistic output (0-1)
- ✓ Simple & interpretable
- ✓ Fast prediction
- ✓ Shows conversion likelihood
- ✗ Assumes linear decision boundary

---

## PRACTICAL WORKFLOW

1. **New Session Arrives** → Loaded into `input.json`
2. **All 3 Models Run** → Each analyzes the session independently
3. **Results Combined** → `reports.py` aggregates findings
4. **5 Reports Generated**:
   - Anomaly Detection Alert ✓
   - Fraud/Bot Detection Alert ✓
   - Conversion Drop Analysis ✓
   - Revenue Leakage Opportunities ✓
   - Data Integrity Issues ✓

5. **Actionable Insights** → Business teams act on results

---

## Summary

| Model | Algorithm | Goal | Impact |
|-------|-----------|------|--------|
| **1. Anomaly** | Isolation Forest | Detect behavioral outliers | Catch unusual sessions |
| **2. Fraud** | Random Forest | Detect bot/fake traffic | Prevent fake conversions |
| **3. Conversion** | Logistic Regression | Predict buyer likelihood | Target high-value users |

Each model serves a distinct purpose in the analytics pipeline, and together they provide comprehensive session monitoring and prediction capabilities.
