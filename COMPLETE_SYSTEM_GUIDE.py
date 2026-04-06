# 🎯 COMPLETE GUIDE: HOW ALL MODELS & REPORTS WORK TOGETHER

"""
════════════════════════════════════════════════════════════════════════════════
                    ANALYTICS ANOMALY DETECTION SYSTEM
════════════════════════════════════════════════════════════════════════════════

You have 3 MODELS and 5 REPORTS. Here's how they ALL connect:
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 1: THE 3 MODELS YOU TRAINED
# ════════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL 1: ANOMALY DETECTION (Isolation Forest)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ File: train_model.py                                                        │
│ Model: ../models/isolation_forest.pkl                                       │
│ Scaler: ../models/scaler.pkl                                                │
│                                                                             │
│ Purpose: Detect BEHAVIORAL ANOMALIES in user sessions                      │
│ Predicts: true/false (is this session anomalous?)                          │
│ Used By: test_model.py                                                      │
│ Risk Levels: Low/Medium/High                                                │
│                                                                             │
│ Analyzes 13 Features:                                                       │
│ • Session metrics (duration, pages, clicks, events, scroll)                │
│ • User history (total sessions, avg duration, avg clicks, conversion)      │
│ • Behavioral ratios (click rate, events per click)                         │
│ • Time (hour of day)                                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL 2: FRAUD DETECTION (Custom Rules + ML)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ File: fraud_model.pkl (pre-trained)                                         │
│ Script: run_fraud.py                                                        │
│ Output: ../models/fraud_output.json                                         │
│                                                                             │
│ Purpose: Detect BOT/FRAUD activity and suspicious patterns                 │
│ Predicts: true/false (is this fraudulent?)                                 │
│ Used By: run_fraud.py                                                       │
│ Fraud Score: 0-6 range                                                      │
│                                                                             │
│ Detects:                                                                    │
│ • Bot activity (extreme clicks in short time)                              │
│ • Extreme events (too many events/second)                                   │
│ • Unrealistic scroll speed (99% in <5 seconds)                             │
│ • Abnormal page loads (50 pages in 30 seconds)                             │
│ • Idle sessions (1000+ seconds with 0 clicks)                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL 3: CONVERSION PREDICTION (Logistic Regression)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ File: train_conversion.py                                                   │
│ Model: ../models/conversion_model.pkl                                       │
│ Scaler: ../models/conversion_scaler.pkl                                     │
│ Script: test_conversion.py                                                  │
│ Output: ../models/conversion_output.json                                    │
│                                                                             │
│ Purpose: PREDICT if a session will convert                                 │
│ Predicts: probability 0-1 (will they buy?)                                 │
│ Used By: test_conversion.py                                                │
│ Likelihood: LOW/MEDIUM/HIGH                                                │
│                                                                             │
│ Analyzes 14 Features:                                                       │
│ • Session engagement (duration, pages, clicks)                             │
│ • User history (conversion rate, avg metrics)                              │
│ • Time patterns (hour, day of week)                                        │
│ • Behavior (click rate, events per click, pages/session)                   │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 2: THE 5 REPORTS & WHAT THEY USE
# ════════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT 1: TRAFFIC SPIKE/DROP ANOMALY                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generated By: reports.py                                                    │
│ Models Used: NONE (Rule-based)                                              │
│ Logic Type: Statistical - compares current vs historical hourly traffic    │
│                                                                             │
│ What It Does:                                                               │
│ ✓ Groups sessions by hour (15:00, 16:00, etc.)                             │
│ ✓ Compares current traffic to historical average                           │
│ ✓ Flags if change > ±50%                                                   │
│                                                                             │
│ Example:                                                                    │
│ Historical hour 15: 417 sessions average                                    │
│ Current hour 15: 1 session                                                  │
│ Result: -99.76% TRAFFIC DROP → ANOMALY ALERT                               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT 2: FRAUD / BOT TRAFFIC DETECTION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generated By: reports.py                                                    │
│ Models Used: RULE-BASED (not ML model)                                      │
│ Logic Type: Heuristic rules + fraud scoring                                 │
│                                                                             │
│ What It Does:                                                               │
│ ✓ Analyzes each session for bot/fraud patterns                             │
│ ✓ Assigns fraud_score (0-6)                                                │
│ ✓ Flags suspicious activity types                                          │
│                                                                             │
│ Fraud Score Rules:                                                          │
│ • 150 clicks in 5 sec → +3 points (BOT)                                    │
│ • 500 events in 8 sec → +3 points (BOT)                                    │
│ • 99% scroll in 3 sec → +2 points (UNREALISTIC)                            │
│ • 50 pages in 30 sec → +2 points (ABNORMAL)                                │
│ • 1200 sec, 0 clicks → +2 points (IDLE)                                    │
│ → Fraud Score ≥ 1 = FRAUD ALERT                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT 3: CONVERSION DROP ALERTS                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generated By: reports.py                                                    │
│ Models Used: NONE (Statistical comparison)                                  │
│ Logic Type: Rate comparison - current vs historical                         │
│                                                                             │
│ What It Does:                                                               │
│ ✓ Calculates historical conversion rate (from 10k dataset)                 │
│ ✓ Calculates current conversion rate (from input.json)                     │
│ ✓ Measures the drop percentage                                              │
│ ✓ Alert levels: LOW (<2%), MEDIUM (2-5%), HIGH (>5%)                      │
│                                                                             │
│ Example:                                                                    │
│ Historical: 11.35% converted                                                │
│ Current: 0% converted (0 out of 1 sessions)                                │
│ Drop: 11.35% → HIGH ALERT                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT 4: REVENUE LEAKAGE DETECTION                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generated By: reports.py                                                    │
│ Models Used: NONE (Rule-based)                                              │
│ Logic Type: Feature analysis - engagement without conversion                │
│                                                                             │
│ What It Does:                                                               │
│ ✓ Identifies sessions with good engagement but NO conversion               │
│ ✓ Flags potential lost revenue opportunities                                │
│ ✓ Risk levels: HIGH/MEDIUM/LOW                                              │
│                                                                             │
│ Risk Scoring:                                                               │
│ • Long duration (600+s) + 20 pages + NO conversion → +2 HIGH RISK          │
│ • High clicks (150+) + NO conversion → +2 MEDIUM RISK                      │
│ • 95%+ scroll depth + NO conversion → +1 MEDIUM RISK                       │
│ • Total ≥ 4 = HIGH RISK | ≥ 2 = MEDIUM RISK                               │
│                                                                             │
│ Example:                                                                    │
│ Session: 550 sec duration, 15 pages, 95% scroll, 40 clicks, NOT converted  │
│ → MEDIUM/HIGH RISK for revenue leakage                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ REPORT 5: DATA INTEGRITY & TRACKING ISSUES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Generated By: reports.py                                                    │
│ Models Used: NONE (Validation rules)                                        │
│ Logic Type: Data quality checks                                             │
│                                                                             │
│ What It Does:                                                               │
│ ✓ Validates data for logical consistency                                   │
│ ✓ Detects tracking/measurement errors                                       │
│ ✓ Severity levels: CRITICAL, WARNING, INFO                                  │
│                                                                             │
│ Checks Performed:                                                           │
│ CRITICAL Issues:                                                            │
│  • Negative duration (-100) → Invalid data                                  │
│  • Negative metrics (clicks: -15) → Invalid tracking                        │
│                                                                             │
│ WARNING Issues:                                                             │
│  • 1000 sec session, 0 pages → Idle/stuck session                          │
│  • 0 events recorded in 300s → Missing tracking                            │
│  • 100 clicks but only 20 events → Ratio mismatch                          │
│                                                                             │
│ INFO Issues:                                                                │
│  • Converted but 0% scroll depth → Unusual but possible                     │
│                                                                             │
│ Data Quality Score = (Sessions without issues / Total) × 100%              │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 3: COMPLETE WORKFLOW
# ════════════════════════════════════════════════════════════════════════════════

"""
INPUT.JSON (Your Test Data)
         ↓
    ┌────────────────────────────────────────────────────────┐
    │         reports.py (Main Report Engine)                │
    │  • Loads input.json                                    │
    │  • Loads historical data (10k.csv)                     │
    │  • Applies feature engineering                          │
    └────────────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────────────┐
    │ PROCESSES 5 INDEPENDENT REPORTS:                        │
    ├─────────────────────────────────────────────────────────┤
    │ 1. Traffic Spike/Drop (hourly comparison)               │
    │ 2. Fraud/Bot Detection (rule-based scoring)             │
    │ 3. Conversion Drop (rate comparison)                    │
    │ 4. Revenue Leakage (engagement analysis)                │
    │ 5. Data Integrity (validation checks)                   │
    └─────────────────────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────────────────────┐
    │ OUTPUTS 6 JSON FILES:                                   │
    ├─────────────────────────────────────────────────────────┤
    │ • report_traffic_spike.json                             │
    │ • report_fraud_bot.json                                 │
    │ • report_conversion_drop.json                           │
    │ • report_revenue_leakage.json                           │
    │ • report_data_integrity.json                            │
    │ • combined_report.json (all in one)                     │
    └─────────────────────────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 4: HOW THE 3 MODELS FIT IN
# ════════════════════════════════════════════════════════════════════════════════

"""
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL USAGE MAPPING                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ ANOMALY MODEL (Isolation Forest)                                           │
│ ├─ Used By: test_model.py                                                  │
│ ├─ Output: ../models/output.json                                           │
│ ├─ Attributes: anomaly (true/false), risk_level, anomaly_score             │
│ ├─ Related Report: NONE (separate file)                                    │
│ └─ Purpose: Find unusual user behavior patterns                            │
│                                                                             │
│ FRAUD MODEL (Rule-Based + ML)                                              │
│ ├─ Used By: run_fraud.py                                                   │
│ ├─ Output: ../models/fraud_output.json                                     │
│ ├─ Attributes: fraud (true/false)                                          │
│ ├─ Related Report: REPORT 2 (Fraud Detection in reports.py)               │
│ └─ Purpose: Detect bot/fraud patterns                                      │
│                                                                             │
│ CONVERSION MODEL (Logistic Regression)                                     │
│ ├─ Used By: test_conversion.py                                             │
│ ├─ Output: ../models/conversion_output.json                                │
│ ├─ Attributes: will_convert, conversion_probability, likelihood             │
│ ├─ Related Report: REPORT 3 (Conversion Drop in reports.py)               │
│ └─ Purpose: Predict conversion probability                                 │
│                                                                             │
│ ALL REPORTS                                                                │
│ ├─ Used By: reports.py                                                     │
│ ├─ Outputs: 5 individual reports + 1 combined                              │
│ ├─ Uses Models: NO (rule-based + statistical)                              │
│ └─ Purpose: Comprehensive anomaly detection system                         │
└─────────────────────────────────────────────────────────────────────────────┘
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 5: STEP-BY-STEP HOW TO USE EVERYTHING
# ════════════════════════════════════════════════════════════════════════════════

"""
SCENARIO: You want to test your system with new analytics data

STEP 1: Prepare Test Data
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ Edit: input.json
   ↓
   Add your test sessions (single or multiple)
   
STEP 2a: Get Anomaly Predictions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python test_model.py
   ↓
   Outputs: ../models/output.json
   Contains: anomaly true/false, risk_level, anomaly_score
   
STEP 2b: Get Fraud Predictions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python run_fraud.py
   ↓
   Outputs: ../models/fraud_output.json
   Contains: fraud true/false
   
STEP 2c: Get Conversion Predictions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python test_conversion.py
   ↓
   Outputs: ../models/conversion_output.json
   Contains: will_convert, conversion_probability, likelihood
   
STEP 3: Get All Reports (Comprehensive Insights)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ python reports.py
   ↓
   Outputs 6 files:
   1. report_traffic_spike.json      ← Traffic anomalies
   2. report_fraud_bot.json          ← Bot activity
   3. report_conversion_drop.json    ← Conversion rates
   4. report_revenue_leakage.json    ← Lost revenue risks
   5. report_data_integrity.json     ← Data quality
   6. combined_report.json           ← All 5 reports together
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 6: QUICK REFERENCE - WHAT EACH SCRIPT DOES
# ════════════════════════════════════════════════════════════════════════════════

"""
Scripts Overview:

TRAINING SCRIPTS (Run once to create models):
├─ train_model.py            → Creates anomaly detection model
├─ fraud_model.pkl           → Pre-trained fraud model
└─ train_conversion.py       → Creates conversion prediction model

TESTING/PREDICTION SCRIPTS (Run with input.json):
├─ test_model.py             → Predicts anomalies
├─ run_fraud.py              → Predicts fraud
├─ test_conversion.py        → Predicts conversions
└─ reports.py                → Generates 5 comprehensive reports

REFERENCE/DOCUMENTATION:
├─ MANUAL_TEST_GUIDE.py      → Detailed test data for each report
└─ QUICK_TEST_REFERENCE.md   → Quick copy-paste test data
"""

# ════════════════════════════════════════════════════════════════════════════════
# PART 7: EXAMPLE COMPLETE FLOW
# ════════════════════════════════════════════════════════════════════════════════

"""
EXAMPLE WORKFLOW (All steps):

1) Edit input.json with test data →
   [{"session_id": "s1", "visitor_id": "u1", ...}]

2) Run anomaly detection →
   python test_model.py
   Output: anomaly true/false

3) Run fraud detection →
   python run_fraud.py
   Output: fraud true/false

4) Run conversion prediction →
   python test_conversion.py
   Output: will_convert + probability

5) Run ALL reports →
   python reports.py
   Outputs: 6 JSON files with all insights
   
   Example Report Output:
   ✓ Traffic Spike: Detected 1 anomaly in hour 15
   ✓ Fraud: 0 fraudulent sessions
   ✓ Conversion Drop: HIGH alert (11.35% drop)
   ✓ Revenue Leakage: 0 high-risk sessions
   ✓ Data Integrity: 100% quality score

Then you can:
├─ View combined_report.json for overview
├─ Check individual report files for details
├─ Make business decisions based on alerts
└─ Take action (block fraudsters, optimize funnel, etc.)
"""

print("""
════════════════════════════════════════════════════════════════════════════════
                            SUMMARY
════════════════════════════════════════════════════════════════════════════════

✅ YOU HAVE 3 MODELS:
   1. Anomaly Detection (test_model.py)
   2. Fraud Detection (run_fraud.py)
   3. Conversion Prediction (test_conversion.py)

✅ YOU HAVE 5 COMPREHENSIVE REPORTS (via reports.py):
   1. Traffic Spike/Drop Anomaly
   2. Fraud / Bot Traffic Detection
   3. Conversion Drop Alerts
   4. Revenue Leakage Detection
   5. Data Integrity & Tracking Issues

✅ QUICK COMMANDS:
   python test_model.py          → Anomaly predictions
   python run_fraud.py           → Fraud predictions
   python test_conversion.py     → Conversion predictions
   python reports.py             → ALL 5 reports
   
   cat ../models/combined_report.json → View all insights

✅ NEXT STEP:
   Choose a test from QUICK_TEST_REFERENCE.md
   Paste into input.json
   Run: python reports.py
   Check the generated reports!

════════════════════════════════════════════════════════════════════════════════
""")
