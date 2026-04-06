# 🧪 MANUAL TESTING GUIDE FOR EACH REPORT

## Test Structure:
# 1. Edit input.json with test data
# 2. Run: python reports.py
# 3. Check: ../models/report_*.json files
# 4. Verify expected output

# =====================================================================
# REPORT 1: TRAFFIC SPIKE/DROP ANOMALY
# =====================================================================
# Tests detection of unusual traffic per hour
# Threshold: >50% change from historical average

# TEST 1.1: TRAFFIC SPIKE (High traffic in one hour)
TEST_1_1 = """
[
  {
    "session_id": "spike_001",
    "visitor_id": "u_spike_1",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:30:00",
    "session_duration": 200,
    "pages_viewed": 3,
    "scroll_depth": 60,
    "clicks": 5,
    "events_count": 10,
    "converted": false
  },
  {
    "session_id": "spike_002",
    "visitor_id": "u_spike_2",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:45:00",
    "session_duration": 250,
    "pages_viewed": 4,
    "scroll_depth": 70,
    "clicks": 8,
    "events_count": 15,
    "converted": false
  },
  {
    "session_id": "spike_003",
    "visitor_id": "u_spike_3",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:50:00",
    "session_duration": 300,
    "pages_viewed": 5,
    "scroll_depth": 80,
    "clicks": 10,
    "events_count": 20,
    "converted": false
  }
]
"""
# EXPECTED OUTPUT: 
# hour_15: status = "SPIKE", percent_change = positive large number

# =====================================================================
# REPORT 2: FRAUD / BOT TRAFFIC DETECTION
# =====================================================================
# Tests detection of automated/bot behavior

# TEST 2.1: EXTREME CLICKS IN SHORT TIME (Classic Bot)
TEST_2_1 = """
[
  {
    "session_id": "bot_001",
    "visitor_id": "u_bot",
    "site_id": "site_001",
    "timestamp": "2026-04-07T10:00:00",
    "session_duration": 5,
    "pages_viewed": 1,
    "scroll_depth": 50,
    "clicks": 150,
    "events_count": 100,
    "converted": false
  }
]
"""
# EXPECTED: fraudulent_sessions: 1, fraud_rate: 100%
# FLAG: "bot_activity_extreme_clicks"

# TEST 2.2: EXTREME EVENTS IN SHORT TIME
TEST_2_2 = """
[
  {
    "session_id": "bot_002",
    "visitor_id": "u_bot_events",
    "site_id": "site_001",
    "timestamp": "2026-04-07T11:00:00",
    "session_duration": 8,
    "pages_viewed": 1,
    "scroll_depth": 40,
    "clicks": 10,
    "events_count": 500,
    "converted": false
  }
]
"""
# EXPECTED: fraudulent_sessions: 1
# FLAG: "bot_activity_extreme_events"

# TEST 2.3: UNREALISTIC SCROLL SPEED
TEST_2_3 = """
[
  {
    "session_id": "bot_003",
    "visitor_id": "u_bot_scroll",
    "site_id": "site_001",
    "timestamp": "2026-04-07T12:00:00",
    "session_duration": 3,
    "pages_viewed": 1,
    "scroll_depth": 99,
    "clicks": 5,
    "events_count": 10,
    "converted": false
  }
]
"""
# EXPECTED: fraudulent_sessions: 1
# FLAG: "unrealistic_scroll_speed"

# TEST 2.4: ABNORMAL PAGE LOAD SPEED
TEST_2_4 = """
[
  {
    "session_id": "bot_004",
    "visitor_id": "u_bot_pages",
    "site_id": "site_001",
    "timestamp": "2026-04-07T13:00:00",
    "session_duration": 30,
    "pages_viewed": 50,
    "scroll_depth": 60,
    "clicks": 100,
    "events_count": 200,
    "converted": false
  }
]
"""
# EXPECTED: fraudulent_sessions: 1
# FLAG: "abnormal_page_load_speed"

# TEST 2.5: IDLE SESSION (No engagement for long time)
TEST_2_5 = """
[
  {
    "session_id": "bot_005",
    "visitor_id": "u_idle",
    "site_id": "site_001",
    "timestamp": "2026-04-07T14:00:00",
    "session_duration": 1200,
    "pages_viewed": 1,
    "scroll_depth": 5,
    "clicks": 0,
    "events_count": 1,
    "converted": false
  }
]
"""
# EXPECTED: fraudulent_sessions: 1
# FLAG: "idle_session_possible_fraud"

# =====================================================================
# REPORT 3: CONVERSION DROP ALERTS
# =====================================================================
# Tests detection of drop in conversion rate
# Historical conv rate: ~11.35%

# TEST 3.1: NO CONVERSIONS (Triggers HIGH alert)
TEST_3_1 = """
[
  {
    "session_id": "conv_drop_001",
    "visitor_id": "u_no_conv_1",
    "site_id": "site_001",
    "timestamp": "2026-04-07T10:00:00",
    "session_duration": 250,
    "pages_viewed": 4,
    "scroll_depth": 70,
    "clicks": 8,
    "events_count": 15,
    "converted": false
  },
  {
    "session_id": "conv_drop_002",
    "visitor_id": "u_no_conv_2",
    "site_id": "site_001",
    "timestamp": "2026-04-07T10:30:00",
    "session_duration": 300,
    "pages_viewed": 5,
    "scroll_depth": 75,
    "clicks": 10,
    "events_count": 20,
    "converted": false
  }
]
"""
# EXPECTED: conversion_drop_percent > 5%, alert = "HIGH"

# TEST 3.2: MIX OF CONVERSIONS AND NON-CONVERSIONS
TEST_3_2 = """
[
  {
    "session_id": "conv_mix_001",
    "visitor_id": "u_conv_1",
    "site_id": "site_001",
    "timestamp": "2026-04-07T11:00:00",
    "session_duration": 400,
    "pages_viewed": 6,
    "scroll_depth": 85,
    "clicks": 12,
    "events_count": 25,
    "converted": true
  },
  {
    "session_id": "conv_mix_002",
    "visitor_id": "u_conv_2",
    "site_id": "site_001",
    "timestamp": "2026-04-07T11:30:00",
    "session_duration": 350,
    "pages_viewed": 5,
    "scroll_depth": 80,
    "clicks": 10,
    "events_count": 20,
    "converted": true
  }
]
"""
# EXPECTED: current_conversion_rate = 100%, conversion_drop_percent negative

# =====================================================================
# REPORT 4: REVENUE LEAKAGE DETECTION
# =====================================================================
# Tests detection of sessions at risk of abandonment

# TEST 4.1: HIGH ENGAGEMENT NO CONVERSION (Revenue leak)
TEST_4_1 = """
[
  {
    "session_id": "leak_001",
    "visitor_id": "u_leak_1",
    "site_id": "site_001",
    "timestamp": "2026-04-07T12:00:00",
    "session_duration": 550,
    "pages_viewed": 15,
    "scroll_depth": 95,
    "clicks": 40,
    "events_count": 80,
    "converted": false
  }
]
"""
# EXPECTED: leakage_risk_sessions: 1, HIGH or MEDIUM risk
# FACTORS: "high_engagement_no_conversion"

# TEST 4.2: HIGH SCROLL NO CONVERSION
TEST_4_2 = """
[
  {
    "session_id": "leak_002",
    "visitor_id": "u_leak_2",
    "site_id": "site_001",
    "timestamp": "2026-04-07T13:00:00",
    "session_duration": 300,
    "pages_viewed": 5,
    "scroll_depth": 90,
    "clicks": 8,
    "events_count": 15,
    "converted": false
  }
]
"""
# EXPECTED: leakage_risk_sessions: 1
# FACTORS: "high_scroll_no_conversion"

# TEST 4.3: SHORT DURATION HIGH PAGES
TEST_4_3 = """
[
  {
    "session_id": "leak_003",
    "visitor_id": "u_leak_3",
    "site_id": "site_001",
    "timestamp": "2026-04-07T14:00:00",
    "session_duration": 100,
    "pages_viewed": 20,
    "scroll_depth": 50,
    "clicks": 30,
    "events_count": 50,
    "converted": false
  }
]
"""
# EXPECTED: leakage_risk_sessions: 1
# FACTORS: "short_duration_high_pages"

# =====================================================================
# REPORT 5: DATA INTEGRITY & TRACKING ISSUES
# =====================================================================
# Tests detection of data quality problems

# TEST 5.1: NEGATIVE DURATION (CRITICAL)
TEST_5_1 = """
[
  {
    "session_id": "quality_001",
    "visitor_id": "u_bad",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:00:00",
    "session_duration": -100,
    "pages_viewed": 5,
    "scroll_depth": 60,
    "clicks": 10,
    "events_count": 20,
    "converted": false
  }
]
"""
# EXPECTED: critical_issues: 1, severity: "CRITICAL"
# ISSUE: "invalid_negative_duration"

# TEST 5.2: NEGATIVE METRICS (CRITICAL)
TEST_5_2 = """
[
  {
    "session_id": "quality_002",
    "visitor_id": "u_bad_metrics",
    "site_id": "site_001",
    "timestamp": "2026-04-07T16:00:00",
    "session_duration": 200,
    "pages_viewed": 5,
    "scroll_depth": 60,
    "clicks": -15,
    "events_count": -50,
    "converted": false
  }
]
"""
# EXPECTED: critical_issues: 1
# ISSUE: "negative_metrics"

# TEST 5.3: NO PAGES LONG DURATION (WARNING)
TEST_5_3 = """
[
  {
    "session_id": "quality_003",
    "visitor_id": "u_warning",
    "site_id": "site_001",
    "timestamp": "2026-04-07T17:00:00",
    "session_duration": 1000,
    "pages_viewed": 0,
    "scroll_depth": 0,
    "clicks": 0,
    "events_count": 0,
    "converted": false
  }
]
"""
# EXPECTED: warning_issues: 1
# ISSUE: "no_pages_long_duration"

# TEST 5.4: NO EVENTS RECORDED (WARNING)
TEST_5_4 = """
[
  {
    "session_id": "quality_004",
    "visitor_id": "u_no_events",
    "site_id": "site_001",
    "timestamp": "2026-04-07T18:00:00",
    "session_duration": 300,
    "pages_viewed": 5,
    "scroll_depth": 60,
    "clicks": 10,
    "events_count": 0,
    "converted": false
  }
]
"""
# EXPECTED: warning_issues: 1
# ISSUE: "no_events_recorded"

# TEST 5.5: CONVERSION NO ENGAGEMENT (INFO)
TEST_5_5 = """
[
  {
    "session_id": "quality_005",
    "visitor_id": "u_info",
    "site_id": "site_001",
    "timestamp": "2026-04-07T19:00:00",
    "session_duration": 10,
    "pages_viewed": 1,
    "scroll_depth": 0,
    "clicks": 0,
    "events_count": 0,
    "converted": true
  }
]
"""
# EXPECTED: sessions_with_issues: 1, severity: "INFO"
# ISSUE: "conversion_no_engagement"

# TEST 5.6: CLICKS EXCEED EVENTS RATIO (WARNING)
TEST_5_6 = """
[
  {
    "session_id": "quality_006",
    "visitor_id": "u_ratio",
    "site_id": "site_001",
    "timestamp": "2026-04-07T20:00:00",
    "session_duration": 300,
    "pages_viewed": 5,
    "scroll_depth": 60,
    "clicks": 100,
    "events_count": 20,
    "converted": false
  }
]
"""
# EXPECTED: warning_issues: 1
# ISSUE: "clicks_exceed_events_ratio"

# =====================================================================
# COMBINED TEST: ALL ISSUES AT ONCE
# =====================================================================

COMBINED_TEST = """
[
  {
    "session_id": "combined_bot",
    "visitor_id": "u_bot_combined",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:30:00",
    "session_duration": 5,
    "pages_viewed": 1,
    "scroll_depth": 99,
    "clicks": 500,
    "events_count": 1000,
    "converted": false
  },
  {
    "session_id": "combined_leak",
    "visitor_id": "u_leak_combined",
    "site_id": "site_001",
    "timestamp": "2026-04-07T15:45:00",
    "session_duration": 800,
    "pages_viewed": 20,
    "scroll_depth": 99,
    "clicks": 100,
    "events_count": 200,
    "converted": false
  },
  {
    "session_id": "combined_bad",
    "visitor_id": "u_bad_combined",
    "site_id": "site_001",
    "timestamp": "2026-04-07T16:00:00",
    "session_duration": -50,
    "pages_viewed": 10,
    "scroll_depth": 150,
    "clicks": -30,
    "events_count": -100,
    "converted": false
  }
]
"""
# EXPECTED: Multiple alerts across all 5 reports!

# =====================================================================
# HOW TO RUN TESTS
# =====================================================================

# STEP 1: Copy test data from above
# STEP 2: Paste into input.json
# STEP 3: Run: python reports.py
# STEP 4: Check specific report file
#         cat ../models/report_fraud_bot.json
# STEP 5: Verify expected output matches

# EXAMPLE WORKFLOW:
#
# 1. Test Fraud Detection:
#    a) Copy TEST_2_1 to input.json
#    b) python reports.py
#    c) Check: fraudulent_sessions should be 1
#
# 2. Test Revenue Leakage:
#    a) Copy TEST_4_1 to input.json
#    b) python reports.py
#    c) Check: leakage_risk_sessions should be 1
#
# 3. Test Data Integrity:
#    a) Copy TEST_5_1 to input.json
#    b) python reports.py
#    c) Check: critical_issues should be 1

print("""
╔════════════════════════════════════════════════════════════════════╗
║          MANUAL TESTING GUIDE - TEST EACH REPORT                  ║
╚════════════════════════════════════════════════════════════════════╝

QUICK START:
1. Open: input.json
2. Replace content with test data (see above)
3. Run: python reports.py
4. Check: ../models/report_*.json files
5. Verify output matches expected results

TEST CATEGORIES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  TRAFFIC SPIKE/DROP
   Use: TEST_1_1
   Expected: hour_15 with positive spike value

2️⃣  FRAUD / BOT DETECTION
   Use: TEST_2_1, TEST_2_2, TEST_2_3, TEST_2_4, or TEST_2_5
   Expected: fraudulent_sessions > 0, specific flags

3️⃣  CONVERSION DROP
   Use: TEST_3_1 or TEST_3_2
   Expected: high alert if no conversions, conversion_drop > 5%

4️⃣  REVENUE LEAKAGE
   Use: TEST_4_1, TEST_4_2, or TEST_4_3
   Expected: leakage_risk_sessions > 0

5️⃣  DATA INTEGRITY
   Use: TEST_5_1 through TEST_5_6
   Expected: critical/warning issues detected

🎯 COMBINED TEST:
   Use: COMBINED_TEST
   Expected: Multiple alerts across all reports

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Each test is self-contained and demonstrates specific detection logic.
""")
