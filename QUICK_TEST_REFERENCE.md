# 📋 QUICK MANUAL TESTING CHECKLIST

## 🚀 GENERAL WORKFLOW FOR ANY TEST:

```
STEP 1: Edit input.json
STEP 2: Run: python reports.py
STEP 3: Check generated reports
STEP 4: Verify expected behavior
```

---

## 🧪 TEST 1: TRAFFIC SPIKE/DROP ANOMALY

**What it detects:** Unusual traffic per hour (+/- 50% from average)

**Step 1: Edit input.json**
```json
[
  {"session_id": "s1", "visitor_id": "u1", "site_id": "site_001", 
   "timestamp": "2026-04-07T15:00:00", "session_duration": 200, 
   "pages_viewed": 3, "scroll_depth": 60, "clicks": 5, "events_count": 10, "converted": false},
  {"session_id": "s2", "visitor_id": "u2", "site_id": "site_001", 
   "timestamp": "2026-04-07T15:15:00", "session_duration": 250, 
   "pages_viewed": 4, "scroll_depth": 70, "clicks": 8, "events_count": 15, "converted": false},
  {"session_id": "s3", "visitor_id": "u3", "site_id": "site_001", 
   "timestamp": "2026-04-07T15:30:00", "session_duration": 300, 
   "pages_viewed": 5, "scroll_depth": 80, "clicks": 10, "events_count": 20, "converted": false}
]
```

**Step 2: Run**
```bash
python reports.py
```

**Step 3: Check**
```bash
cat ../models/report_traffic_spike.json
```

**Step 4: Expected Output**
```json
{
  "hour_15": {
    "status": "SPIKE",
    "percent_change": "positive value > 50",
    "anomaly": true
  }
}
```

---

## 🧪 TEST 2: FRAUD / BOT DETECTION

**What it detects:** Automated/bot behavior patterns

### **Test 2A: Bot with extreme clicks**
```json
[
  {"session_id": "bot_test", "visitor_id": "u_bot", "site_id": "site_001",
   "timestamp": "2026-04-07T10:00:00", "session_duration": 5,
   "pages_viewed": 1, "scroll_depth": 50, "clicks": 150, "events_count": 100, "converted": false}
]
```
**Expected:** fraudulent_sessions: 1, Flag: "bot_activity_extreme_clicks"

### **Test 2B: Unrealistic scroll speed**
```json
[
  {"session_id": "scroll_test", "visitor_id": "u_scroll", "site_id": "site_001",
   "timestamp": "2026-04-07T11:00:00", "session_duration": 3,
   "pages_viewed": 1, "scroll_depth": 99, "clicks": 5, "events_count": 10, "converted": false}
]
```
**Expected:** fraudulent_sessions: 1, Flag: "unrealistic_scroll_speed"

### **Test 2C: Idle session (long duration, no engagement)**
```json
[
  {"session_id": "idle_test", "visitor_id": "u_idle", "site_id": "site_001",
   "timestamp": "2026-04-07T12:00:00", "session_duration": 1200,
   "pages_viewed": 1, "scroll_depth": 5, "clicks": 0, "events_count": 1, "converted": false}
]
```
**Expected:** fraudulent_sessions: 1, Flag: "idle_session_possible_fraud"

---

## 🧪 TEST 3: CONVERSION DROP ALERTS

**What it detects:** Changes in conversion rate (HIGH alert if >5% drop)

### **Test 3A: No conversions**
```json
[
  {"session_id": "no_conv_1", "visitor_id": "u1", "site_id": "site_001",
   "timestamp": "2026-04-07T10:00:00", "session_duration": 250,
   "pages_viewed": 4, "scroll_depth": 70, "clicks": 8, "events_count": 15, "converted": false},
  {"session_id": "no_conv_2", "visitor_id": "u2", "site_id": "site_001",
   "timestamp": "2026-04-07T10:30:00", "session_duration": 300,
   "pages_viewed": 5, "scroll_depth": 75, "clicks": 10, "events_count": 20, "converted": false}
]
```

**Check**
```bash
cat ../models/report_conversion_drop.json
```

**Expected:**
```json
{
  "historical_conversion_rate": 11.35,
  "current_conversion_rate": 0.0,
  "conversion_drop_percent": 11.35,
  "alert": "HIGH"
}
```

---

## 🧪 TEST 4: REVENUE LEAKAGE DETECTION

**What it detects:** Sessions at risk of abandonment/not converting

### **Test 4A: High engagement but no conversion**
```json
[
  {"session_id": "leak_test", "visitor_id": "u_leak", "site_id": "site_001",
   "timestamp": "2026-04-07T12:00:00", "session_duration": 550,
   "pages_viewed": 15, "scroll_depth": 95, "clicks": 40, "events_count": 80, "converted": false}
]
```

**Expected:** leakage_risk_sessions: 1, Factor: "high_engagement_no_conversion"

### **Test 4B: High scroll depth without conversion**
```json
[
  {"session_id": "scroll_leak", "visitor_id": "u_scroll_leak", "site_id": "site_001",
   "timestamp": "2026-04-07T13:00:00", "session_duration": 300,
   "pages_viewed": 5, "scroll_depth": 90, "clicks": 8, "events_count": 15, "converted": false}
]
```

**Expected:** leakage_risk_sessions: 1, Factor: "high_scroll_no_conversion"

---

## 🧪 TEST 5: DATA INTEGRITY & TRACKING ISSUES

**What it detects:** Data quality problems (CRITICAL, WARNING, INFO levels)

### **Test 5A: Negative duration (CRITICAL)**
```json
[
  {"session_id": "bad_data_1", "visitor_id": "u_bad", "site_id": "site_001",
   "timestamp": "2026-04-07T15:00:00", "session_duration": -100,
   "pages_viewed": 5, "scroll_depth": 60, "clicks": 10, "events_count": 20, "converted": false}
]
```

**Expected:** 
```json
{
  "critical_issues": 1,
  "issues": [{"issue": "invalid_negative_duration", "severity": "CRITICAL"}]
}
```

### **Test 5B: Negative metrics (CRITICAL)**
```json
[
  {"session_id": "bad_data_2", "visitor_id": "u_neg_metrics", "site_id": "site_001",
   "timestamp": "2026-04-07T16:00:00", "session_duration": 200,
   "pages_viewed": 5, "scroll_depth": 60, "clicks": -15, "events_count": -50, "converted": false}
]
```

**Expected:** critical_issues: 1, Issue: "negative_metrics"

### **Test 5C: No engagement in long session (WARNING)**
```json
[
  {"session_id": "no_engage", "visitor_id": "u_no_engage", "site_id": "site_001",
   "timestamp": "2026-04-07T17:00:00", "session_duration": 1000,
   "pages_viewed": 0, "scroll_depth": 0, "clicks": 0, "events_count": 0, "converted": false}
]
```

**Expected:** warning_issues: 1, Issue: "no_pages_long_duration"

### **Test 5D: Clicks exceed events ratio (WARNING)**
```json
[
  {"session_id": "bad_ratio", "visitor_id": "u_ratio", "site_id": "site_001",
   "timestamp": "2026-04-07T18:00:00", "session_duration": 300,
   "pages_viewed": 5, "scroll_depth": 60, "clicks": 100, "events_count": 20, "converted": false}
]
```

**Expected:** warning_issues: 1, Issue: "clicks_exceed_events_ratio"

---

## 🎯 COMPREHENSIVE TEST (All Issues)

**Test everything at once:**
```json
[
  {
    "session_id": "bot_all", "visitor_id": "u_bot_all", "site_id": "site_001",
    "timestamp": "2026-04-07T15:30:00", "session_duration": 5,
    "pages_viewed": 1, "scroll_depth": 99, "clicks": 500, "events_count": 1000, "converted": false
  },
  {
    "session_id": "leak_all", "visitor_id": "u_leak_all", "site_id": "site_001",
    "timestamp": "2026-04-07T15:45:00", "session_duration": 800,
    "pages_viewed": 20, "scroll_depth": 99, "clicks": 100, "events_count": 200, "converted": false
  },
  {
    "session_id": "bad_all", "visitor_id": "u_bad_all", "site_id": "site_001",
    "timestamp": "2026-04-07T16:00:00", "session_duration": -50,
    "pages_viewed": 10, "scroll_depth": 150, "clicks": -30, "events_count": -100, "converted": false
  }
]
```

**Check all reports**
```bash
cat ../models/report_fraud_bot.json
cat ../models/report_revenue_leakage.json
cat ../models/report_data_integrity.json
cat ../models/combined_report.json
```

---

## ⏱️ QUICK COMMANDS

```bash
# Run report generator
python reports.py

# View fraud report
cat ../models/report_fraud_bot.json

# View all reports combined
cat ../models/combined_report.json

# View specific report
cat ../models/report_conversion_drop.json
cat ../models/report_traffic_spike.json
cat ../models/report_revenue_leakage.json
cat ../models/report_data_integrity.json
```

---

## ✅ VERIFICATION CHECKLIST

After each test, verify:
- [ ] Report file was created
- [ ] Timestamp is current
- [ ] Expected alerts/detections present
- [ ] Risk levels are correct
- [ ] All sessions accounted for
- [ ] JSON format is valid
