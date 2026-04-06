# 📊 VISUAL SYSTEM ARCHITECTURE & FLOW

```
═══════════════════════════════════════════════════════════════════════════════
                          YOUR COMPLETE SYSTEM
═══════════════════════════════════════════════════════════════════════════════

                              INPUT.JSON
                           (Test Analytics)
                                  ↓
         ┌────────────────────────┼────────────────────────┐
         ↓                        ↓                        ↓
    ┌─────────┐          ┌──────────────┐          ┌─────────────┐
    │  MODEL  │          │  HISTORICAL  │          │    MODEL    │
    │ MODEL 1 │          │     DATA     │          │  MODEL 2 & 3│
    │ANOMALY  │          │  (10k.csv)   │          │ FRAUD & CONV│
    │ FOREST  │          │              │          │             │
    └────┬────┘          └──────┬───────┘          └────┬────────┘
         ↓                       ↓                       ↓
    ┌──────────────┐   ┌────────────────┐   ┌──────────────────┐
    │ test_model   │   │  reports.py    │   │ run_fraud.py     │
    │              │   │  (Main Engine) │   │ test_conv.py     │
    │ → Anomaly    │   │                │   │                  │
    │   Detection  │   │ Processes ALL  │   │ → Fraud Pred     │
    │              │   │                │   │ → Conversion     │
    └──────┬───────┘   └────────┬───────┘   └────────┬─────────┘
           ↓                    ↓                    ↓
    ┌─────────────┐  ┌──────────────────┐  ┌──────────────┐
    │   OUTPUT    │  │   5 REPORTS      │  │   OUTPUTS    │
    │             │  │                  │  │              │
    │output.json  │  │ 1. Traffic       │  │fraud_out.json│
    │             │  │    Spike/Drop    │  │              │
    │ Contains:   │  │                  │  │conv_out.json │
    │ • anomaly   │  │ 2. Fraud/Bot     │  │              │
    │ • risk_lvl  │  │                  │  │ Contains:    │
    │ • anomaly   │  │ 3. Conversion    │  │ • fraud      │
    │   score     │  │    Drop          │  │ • will_conv  │
    │             │  │                  │  │ • prob       │
    └─────────────┘  │ 4. Revenue       │  └──────────────┘
                     │    Leakage       │
                     │                  │
                     │ 5. Data          │
                     │    Integrity     │
                     │                  │
                     │ + combined_      │
                     │   report.json    │
                     └──────────────────┘
```

═══════════════════════════════════════════════════════════════════════════════
                         QUICK START WORKFLOW
═══════════════════════════════════════════════════════════════════════════════

STEP 1: EDIT INPUT DATA
┌─────────────────────────────────────────────────────────────────┐
│ File: input.json                                                │
│                                                                 │
│ Add your test data:                                             │
│ [{                                                              │
│   "session_id": "s1",                                           │
│   "visitor_id": "u1",                                           │
│   "site_id": "site_001",                                        │
│   "timestamp": "2026-04-07T10:00:00",                           │
│   "session_duration": 300,                                      │
│   "pages_viewed": 4,                                            │
│   "scroll_depth": 75,                                           │
│   "clicks": 8,                                                  │
│   "events_count": 20,                                           │
│   "converted": false                                            │
│ }]                                                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
STEP 2: RUN THE REPORTS (FASTEST WAY)
┌─────────────────────────────────────────────────────────────────┐
│ Command: python reports.py                                      │
│                                                                 │
│ This generates ALL 5 reports at once!                           │
│                                                                 │
│ Outputs:                                                        │
│ ✓ report_traffic_spike.json                                    │
│ ✓ report_fraud_bot.json                                        │
│ ✓ report_conversion_drop.json                                  │
│ ✓ report_revenue_leakage.json                                  │
│ ✓ report_data_integrity.json                                   │
│ ✓ combined_report.json                                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
STEP 3: VIEW RESULTS
┌─────────────────────────────────────────────────────────────────┐
│ Quick View:                                                     │
│ $ cat ../models/combined_report.json                            │
│                                                                 │
│ Detailed Views:                                                 │
│ $ cat ../models/report_fraud_bot.json                           │
│ $ cat ../models/report_conversion_drop.json                     │
│ $ cat ../models/report_data_integrity.json                      │
│ etc.                                                            │
│                                                                 │
│ Shows all findings + alerts!                                    │
└─────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                    ALTERNATIVE: INDIVIDUAL MODELS
═══════════════════════════════════════════════════════════════════════════════

If you want individual predictions instead of reports:

OPTION A: Get ANOMALY Score
┌────────────────────────────────────────────────────────────┐
│ $ python test_model.py                                     │
│                                                            │
│ Output: output.json                                        │
│ {                                                          │
│   "session_id": "s1",                                      │
│   "visitor_id": "u1",                                      │
│   "anomaly": false,                                        │
│   "risk_level": "low",                                     │
│   "anomaly_score": -0.05                                   │
│ }                                                          │
└────────────────────────────────────────────────────────────┘

OPTION B: Get FRAUD Score
┌────────────────────────────────────────────────────────────┐
│ $ python run_fraud.py                                      │
│                                                            │
│ Output: fraud_output.json                                  │
│ {                                                          │
│   "session_id": "s1",                                      │
│   "visitor_id": "u1",                                      │
│   "fraud": false                                           │
│ }                                                          │
└────────────────────────────────────────────────────────────┘

OPTION C: Get CONVERSION Probability
┌────────────────────────────────────────────────────────────┐
│ $ python test_conversion.py                                │
│                                                            │
│ Output: conversion_output.json                             │
│ {                                                          │
│   "session_id": "s1",                                      │
│   "visitor_id": "u1",                                      │
│   "will_convert": false,                                   │
│   "conversion_probability": 0.35,                          │
│   "conversion_likelihood": "MEDIUM"                        │
│ }                                                          │
└────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                    WHAT EACH REPORT TELLS YOU
═══════════════════════════════════════════════════════════════════════════════

╔════════════════════════════════════════════════════════════╗
║ REPORT 1: TRAFFIC SPIKE/DROP ANOMALY                      ║
╠════════════════════════════════════════════════════════════╣
║ Tells You: Is traffic unusually high/low in any hour?     ║
║ Alert Threshold: ±50% from historical average              ║
║                                                            ║
║ Example:                                                   ║
║ Hour 15: Avg 417 sessions → Current 1 session              ║
║ Result: 99.76% DROP → ANOMALY ALERT! ⚠️                   ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ REPORT 2: FRAUD / BOT TRAFFIC DETECTION                   ║
╠════════════════════════════════════════════════════════════╣
║ Tells You: Is this automated/bot activity?                ║
║ Flags: Bot clicks, extreme events, unrealistic scrolling   ║
║                                                            ║
║ Example:                                                   ║
║ 5 seconds, 150 clicks → FRAUD DETECTED! 🤖               ║
║ Fraud Score: 3/6 → HIGH RISK ALERT! 🔴                   ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ REPORT 3: CONVERSION DROP ALERTS                          ║
╠════════════════════════════════════════════════════════════╣
║ Tells You: Are conversions dropping?                      ║
║ Alert Levels: HIGH (>5%), MEDIUM (2-5%), LOW (<2%)        ║
║                                                            ║
║ Example:                                                   ║
║ Historical: 11.35% conversion rate                         ║
║ Current: 0% conversion rate                                ║
║ Drop: 11.35% → HIGH ALERT! ⚠️                             ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ REPORT 4: REVENUE LEAKAGE DETECTION                       ║
╠════════════════════════════════════════════════════════════╣
║ Tells You: Which engaged sessions didn't convert?         ║
║ Risk Levels: HIGH, MEDIUM, LOW                             ║
║                                                            ║
║ Example:                                                   ║
║ 550 seconds, 15 pages, 95% scroll, NO conversion          ║
║ Risk: HIGH - Lost revenue opportunity! 💰                 ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ REPORT 5: DATA INTEGRITY & TRACKING ISSUES                ║
╠════════════════════════════════════════════════════════════╣
║ Tells You: Is your data clean/valid?                      ║
║ Severity: CRITICAL, WARNING, INFO                          ║
║ Quality Score: 0-100%                                      ║
║                                                            ║
║ Example:                                                   ║
║ Negative duration: -100 seconds → CRITICAL! 🔴            ║
║ Data Quality: 100% (Perfect!) ✅                          ║
╚════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════════════
                    YOUR SYSTEM FILES AT A GLANCE
═══════════════════════════════════════════════════════════════════════════════

TRAINING FILES (Already done):
├─ train_model.py           → Anomaly model (already trained)
├─ train_conversion.py      → Conversion model (already trained)
└─ fraud_model.pkl          → Fraud model (pre-trained)

TEST/PREDICTION FILES:
├─ test_model.py            → Run anomaly predictions
├─ test_conversion.py       → Run conversion predictions
├─ run_fraud.py             → Run fraud predictions
└─ reports.py               → Generate ALL 5 reports (RECOMMENDED!)

DOCUMENTATION:
├─ COMPLETE_SYSTEM_GUIDE.py → You are here!
├─ MANUAL_TEST_GUIDE.py     → Detailed test cases
└─ QUICK_TEST_REFERENCE.md  → Quick copy-paste tests

DATA FILES:
├─ input.json               → Your test input
├─ analytics_dataset_10k.csv → Historical data for comparison
└─ models/
   ├─ output.json           → Anomaly predictions
   ├─ fraud_output.json     → Fraud predictions
   ├─ conversion_output.json → Conversion predictions
   ├─ report_*.json         → 5 individual reports
   └─ combined_report.json  → All reports together

═══════════════════════════════════════════════════════════════════════════════
                         RECOMMENDED NEXT STEPS
═══════════════════════════════════════════════════════════════════════════════

1. READ THIS FILE (COMPLETE_SYSTEM_GUIDE.py)
   └─ Understand how everything connects

2. OPEN QUICK_TEST_REFERENCE.md
   └─ Copy a test case

3. PASTE INTO input.json
   └─ Replace existing data with test data

4. RUN REPORTS
   └─ python reports.py

5. CHECK RESULTS
   └─ cat ../models/combined_report.json

6. VERIFY ALERTS
   └─ Look for fraud/anomalies/drops in the output

7. ITERATE
   └─ Try different test cases to see different alerts

═══════════════════════════════════════════════════════════════════════════════
"""
