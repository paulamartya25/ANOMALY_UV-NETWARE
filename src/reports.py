import pandas as pd
import numpy as np
import json
import joblib
from datetime import datetime
import os

# ==============================
# REPORTING ENGINE
# ==============================

class AnomalyReporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.models = self._load_models()
        self.data = self._load_data()
        self.metrics = self._load_metrics()
        self.reports = {}
    
    def _load_models(self):
        """Load all trained models"""
        models = {}
        try:
            models['anomaly'] = joblib.load("../models/isolation_forest.pkl")
            models['anomaly_scaler'] = joblib.load("../models/scaler.pkl")
            models['fraud'] = joblib.load("../models/fraud_model.pkl")
            models['conversion'] = joblib.load("../models/conversion_model.pkl")
            models['conversion_scaler'] = joblib.load("../models/conversion_scaler.pkl")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
        return models
    
    def _load_data(self):
        """Load input data"""
        try:
            with open("../data/input.json") as f:
                input_data = json.load(f)
            
            df = pd.DataFrame(input_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Load historical data
            hist_df = pd.read_csv("../data/analytics_dataset_10k.csv")
            hist_df['timestamp'] = pd.to_datetime(hist_df['timestamp'])
            
            return {'input': df, 'historical': hist_df}
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def _load_metrics(self):
        """Load model performance metrics"""
        metrics = {}
        try:
            with open("../models/fraud_metrics.json") as f:
                metrics['fraud'] = json.load(f)
        except Exception as e:
            print(f"⚠️  Fraud metrics not available: {e}")
        
        try:
            with open("../models/conversion_metrics.json") as f:
                metrics['conversion'] = json.load(f)
        except Exception as e:
            print(f"⚠️  Conversion metrics not available: {e}")
        
        return metrics
    
    # ==============================
    # FEATURE ENGINEERING FOR MODELS
    # ==============================
    def _engineer_anomaly_features(self, df, hist_df):
        """Engineer 13 features for anomaly detection model"""
        df_copy = df.copy()
        
        # Visitor-level features from historical data
        visitor_stats = hist_df.groupby("visitor_id").agg({
            "session_id": "count",
            "session_duration": "mean",
            "clicks": "mean",
            "converted": "mean"
        }).rename(columns={
            "session_id": "user_total_sessions",
            "session_duration": "user_avg_duration",
            "clicks": "user_avg_clicks",
            "converted": "user_conversion_rate"
        })
        
        df_copy = df_copy.merge(visitor_stats, on="visitor_id", how="left").fillna(0)
        
        # Time feature
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        
        # Behavioral ratios
        df_copy['click_rate'] = df_copy['clicks'] / (df_copy['session_duration'] + 1)
        df_copy['events_per_click'] = df_copy['events_count'] / (df_copy['clicks'] + 1)
        
        # Sessions per user
        df_copy['sessions_per_user'] = df_copy.groupby("visitor_id")['session_id'].transform('count')
        
        return df_copy
    
    def _engineer_conversion_features(self, df, hist_df):
        """Engineer 14 features for conversion prediction model"""
        df_copy = df.copy()
        
        # Visitor-level stats from historical data
        visitor_stats = hist_df.groupby("visitor_id").agg({
            "session_id": "count",
            "session_duration": "mean",
            "clicks": "mean",
            "converted": "mean"
        }).rename(columns={
            "session_id": "user_total_sessions",
            "session_duration": "user_avg_duration",
            "clicks": "user_avg_clicks",
            "converted": "user_conversion_rate"
        })
        
        df_copy = df_copy.merge(visitor_stats, on="visitor_id", how="left").fillna(0)
        
        # Time features
        df_copy['hour'] = df_copy['timestamp'].dt.hour
        df_copy['day_of_week'] = df_copy['timestamp'].dt.dayofweek
        
        # Behavioral features
        df_copy['click_rate'] = df_copy['clicks'] / (df_copy['session_duration'] + 1)
        df_copy['events_per_click'] = df_copy['events_count'] / (df_copy['clicks'] + 1)
        df_copy['pages_per_session'] = df_copy['pages_viewed'] / (df_copy['session_duration'] + 1)
        
        return df_copy
    
    # ==============================
    # REPORT 1: TRAFFIC SPIKE/DROP ANOMALY
    # ==============================
    def generate_traffic_spike_report(self):
        """Detect traffic spikes and drops"""
        hist = self.data['historical']
        curr = self.data['input']
        
        # Calculate hourly traffic
        hist['hour'] = hist['timestamp'].dt.hour
        hist_traffic = hist.groupby('hour').size()
        
        curr['hour'] = curr['timestamp'].dt.hour
        curr_traffic = curr.groupby('hour').size()
        
        report = {
            "report_type": "Traffic Spike/Drop Anomaly",
            "generated_at": self.timestamp,
            "metrics": {}
        }
        
        # Detect spikes/drops
        for hour in curr_traffic.index:
            if hour in hist_traffic.index:
                hist_avg = hist_traffic[hour]
                curr_val = curr_traffic[hour]
                pct_change = ((curr_val - hist_avg) / hist_avg) * 100
                
                if abs(pct_change) > 50:  # >50% change is anomalous
                    status = "SPIKE" if pct_change > 0 else "DROP"
                    report["metrics"][f"hour_{hour}"] = {
                        "status": status,
                        "historical_avg": int(hist_avg),
                        "current_traffic": int(curr_val),
                        "percent_change": round(pct_change, 2),
                        "anomaly": True
                    }
        
        self.reports['traffic_spike'] = report
        return report
    
    # ==============================
    # REPORT 2: FRAUD / BOT TRAFFIC DETECTION (USING ML MODEL)
    # ==============================
    def generate_fraud_bot_report(self):
        """Detect fraud and bot traffic using the Fraud Detection model"""
        df = self.data['input'].copy()
        hist_df = self.data['historical'].copy()
        
        if df.empty or 'fraud' not in self.models:
            return {"error": "No data or model unavailable"}
        
        # Engineer features for fraud detection
        df['click_rate'] = df['clicks'] / (df['session_duration'] + 1)
        df['events_per_click'] = df['events_count'] / (df['clicks'] + 1)
        
        # Features required by fraud model (4 features)
        fraud_features = [
            "session_duration",
            "clicks",
            "events_count",
            "click_rate"
        ]
        
        X_fraud = df[fraud_features].fillna(0)
        
        # Get fraud predictions from the model
        try:
            fraud_predictions = self.models['fraud'].predict(X_fraud)
            fraud_probabilities = self.models['fraud'].predict_proba(X_fraud)[:, 1]
        except Exception as e:
            print(f"❌ Error running fraud model: {e}")
            fraud_predictions = [0] * len(df)
            fraud_probabilities = [0.0] * len(df)
        
        # Map predictions to sessions
        fraud_indicators = []
        for idx, row in df.iterrows():
            is_fraud = fraud_predictions[idx]
            fraud_prob = fraud_probabilities[idx]
            
            indicators = {
                "session_id": row['session_id'],
                "visitor_id": row['visitor_id'],
                "is_fraudulent": bool(is_fraud),
                "fraud_probability": float(fraud_prob),
                "fraud_confidence": "HIGH" if fraud_prob > 0.7 else ("MEDIUM" if fraud_prob > 0.4 else "LOW"),
                "model_prediction": "BOT/FRAUD DETECTED" if is_fraud else "LEGITIMATE"
            }
            
            if is_fraud:
                fraud_indicators.append(indicators)
        
        report = {
            "report_type": "Fraud / Bot Traffic Detection (ML Model)",
            "generated_at": self.timestamp,
            "model_used": "RandomForestClassifier",
            "total_sessions_analyzed": len(df),
            "fraudulent_sessions": len(fraud_indicators),
            "fraud_rate_percent": round((len(fraud_indicators) / len(df)) * 100, 2) if len(df) > 0 else 0,
            "detections": fraud_indicators,
            "high_confidence_fraud": len([x for x in fraud_indicators if x['fraud_confidence'] == 'HIGH']),
            "medium_confidence_fraud": len([x for x in fraud_indicators if x['fraud_confidence'] == 'MEDIUM']),
            "model_performance": self.metrics.get('fraud', {})
        }
        
        self.reports['fraud_bot'] = report
        return report
    
    # ==============================
    # REPORT 3: CONVERSION DROP ALERTS (USING ML MODEL)
    # ==============================
    def generate_conversion_drop_report(self):
        """Detect conversion drops using Conversion Prediction model"""
        hist = self.data['historical']
        curr = self.data['input'].copy()
        
        if curr.empty or 'conversion' not in self.models:
            return {"error": "No data or model unavailable"}
        
        # Engineer features for conversion prediction (14 features)
        curr = self._engineer_conversion_features(curr, hist)
        
        conversion_features = [
            "session_duration", "pages_viewed", "scroll_depth",
            "clicks", "events_count",
            "user_total_sessions", "user_avg_duration",
            "user_avg_clicks", "user_conversion_rate",
            "hour", "day_of_week", "click_rate",
            "events_per_click", "pages_per_session"
        ]
        
        X_conversion = curr[conversion_features].fillna(0)
        
        # Get conversion predictions from the model
        try:
            X_conversion_scaled = self.models['conversion_scaler'].transform(X_conversion)
            conversion_predictions = self.models['conversion'].predict(X_conversion_scaled)
            conversion_probabilities = self.models['conversion'].predict_proba(X_conversion_scaled)[:, 1]
        except Exception as e:
            print(f"❌ Error running conversion model: {e}")
            conversion_predictions = [0] * len(curr)
            conversion_probabilities = [0.0] * len(curr)
        
        # Historical conversion rate
        hist_conv_rate = (hist['converted'].sum() / len(hist)) * 100
        
        # Current conversion rate from actual data
        actual_conv_rate = (curr['converted'].sum() / len(curr)) * 100 if len(curr) > 0 else 0
        
        # Model-predicted conversion rate
        model_pred_conv_rate = (conversion_probabilities.sum() / len(curr)) * 100 if len(curr) > 0 else 0
        
        # Calculate drops
        actual_drop = hist_conv_rate - actual_conv_rate
        model_drop = hist_conv_rate - model_pred_conv_rate
        
        # Detail by session
        conversion_details = []
        for idx, row in curr.iterrows():
            pred_prob = conversion_probabilities[idx]
            conversion_details.append({
                "session_id": row['session_id'],
                "visitor_id": row['visitor_id'],
                "actual_converted": bool(row['converted']),
                "predicted_conversion_probability": float(pred_prob),
                "predicted_likelihood": "HIGH" if pred_prob > 0.67 else ("MEDIUM" if pred_prob > 0.33 else "LOW")
            })
        
        report = {
            "report_type": "Conversion Drop Alerts (ML Prediction)",
            "generated_at": self.timestamp,
            "model_used": "LogisticRegression",
            "historical_conversion_rate": round(hist_conv_rate, 2),
            "actual_current_conversion_rate": round(actual_conv_rate, 2),
            "model_predicted_conversion_rate": round(model_pred_conv_rate, 2),
            "actual_conversion_drop_percent": round(actual_drop, 2),
            "model_predicted_drop_percent": round(model_drop, 2),
            "actual_alert_level": "HIGH" if actual_drop > 5 else ("MEDIUM" if actual_drop > 2 else "LOW"),
            "model_alert_level": "HIGH" if model_drop > 5 else ("MEDIUM" if model_drop > 2 else "LOW"),
            "sessions_analyzed": len(curr),
            "sessions_actually_converted": len(curr[curr['converted'] == True]),
            "sessions_model_predicted_high_conversion": len([x for x in conversion_details if x['predicted_likelihood'] == 'HIGH']),
            "session_details": conversion_details,
            "model_performance": self.metrics.get('conversion', {})
        }
        
        self.reports['conversion_drop'] = report
        return report
    
    # ==============================
    # REPORT 4: REVENUE LEAKAGE DETECTION (USING ML MODELS)
    # ==============================
    def generate_revenue_leakage_report(self):
        """Detect revenue leakage using Conversion & Anomaly models"""
        hist = self.data['historical']
        curr = self.data['input'].copy()
        
        if curr.empty:
            return {"error": "No data available"}
        
        # Engineer features for conversion prediction
        curr = self._engineer_conversion_features(curr, hist)
        
        conversion_features = [
            "session_duration", "pages_viewed", "scroll_depth",
            "clicks", "events_count",
            "user_total_sessions", "user_avg_duration",
            "user_avg_clicks", "user_conversion_rate",
            "hour", "day_of_week", "click_rate",
            "events_per_click", "pages_per_session"
        ]
        
        X_conversion = curr[conversion_features].fillna(0)
        
        # Get conversion predictions
        try:
            X_conversion_scaled = self.models['conversion_scaler'].transform(X_conversion)
            conversion_probabilities = self.models['conversion'].predict_proba(X_conversion_scaled)[:, 1]
        except Exception as e:
            print(f"❌ Error running conversion model: {e}")
            conversion_probabilities = [0.0] * len(curr)
        
        # Identify leakage: High conversion probability but NOT actually converted
        leakage_indicators = []
        
        for idx, row in curr.iterrows():
            pred_conversion_prob = conversion_probabilities[idx]
            
            # Leakage = model predicts high conversion but didn't actually convert
            if pred_conversion_prob > 0.67 and row['converted'] == False:
                indicator = {
                    "session_id": row['session_id'],
                    "visitor_id": row['visitor_id'],
                    "predicted_conversion_probability": float(pred_conversion_prob),
                    "actually_converted": False,
                    "leakage_severity": "CRITICAL",
                    "lost_opportunity": "HIGH VALUE SESSION - Should have converted"
                }
                leakage_indicators.append(indicator)
            
            elif pred_conversion_prob > 0.33 and row['converted'] == False:
                indicator = {
                    "session_id": row['session_id'],
                    "visitor_id": row['visitor_id'],
                    "predicted_conversion_probability": float(pred_conversion_prob),
                    "actually_converted": False,
                    "leakage_severity": "MEDIUM",
                    "lost_opportunity": "POTENTIAL REVENUE LOSS"
                }
                leakage_indicators.append(indicator)
        
        report = {
            "report_type": "Revenue Leakage Detection (ML-Based)",
            "generated_at": self.timestamp,
            "model_used": "LogisticRegression (Conversion Prediction)",
            "total_sessions": len(curr),
            "leakage_risk_sessions": len(leakage_indicators),
            "critical_leakage_sessions": len([x for x in leakage_indicators if x['leakage_severity'] == 'CRITICAL']),
            "medium_leakage_sessions": len([x for x in leakage_indicators if x['leakage_severity'] == 'MEDIUM']),
            "estimated_lost_opportunity_sessions": len(leakage_indicators),
            "indicators": leakage_indicators
        }
        
        self.reports['revenue_leakage'] = report
        return report
    
    # ==============================
    # REPORT 5: BEHAVIORAL ANOMALY DETECTION (USING ML MODEL)
    # ==============================
    def generate_anomaly_detection_report(self):
        """Detect behavioral anomalies using Isolation Forest model"""
        curr = self.data['input'].copy()
        hist = self.data['historical']
        
        if curr.empty or 'anomaly' not in self.models or 'anomaly_scaler' not in self.models:
            return {"error": "No data or model unavailable"}
        
        # Engineer 13 features for anomaly detection
        curr = self._engineer_anomaly_features(curr, hist)
        
        anomaly_features = [
            "session_duration", "pages_viewed", "scroll_depth",
            "clicks", "events_count",
            "user_total_sessions", "user_avg_duration",
            "user_avg_clicks", "user_conversion_rate",
            "sessions_per_user", "click_rate",
            "events_per_click", "hour"
        ]
        
        X_anomaly = curr[anomaly_features].fillna(0)
        
        # Get anomaly predictions from the model
        try:
            X_anomaly_scaled = self.models['anomaly_scaler'].transform(X_anomaly)
            anomaly_predictions = self.models['anomaly'].predict(X_anomaly_scaled)
            anomaly_scores = self.models['anomaly'].score_samples(X_anomaly_scaled)
        except Exception as e:
            print(f"❌ Error running anomaly model: {e}")
            anomaly_predictions = [1] * len(curr)  # -1 = anomaly
            anomaly_scores = [0.0] * len(curr)
        
        # Map predictions to sessions
        anomaly_indicators = []
        for idx, row in curr.iterrows():
            is_anomalous = anomaly_predictions[idx] == -1
            anomaly_score = anomaly_scores[idx]
            
            if is_anomalous:
                # Lower scores = more anomalous
                if anomaly_score < -0.5:
                    risk_level = "HIGH"
                elif anomaly_score < 0:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
                
                indicator = {
                    "session_id": row['session_id'],
                    "visitor_id": row['visitor_id'],
                    "is_anomalous": True,
                    "anomaly_score": float(anomaly_score),
                    "risk_level": risk_level,
                    "behavioral_pattern": "ANOMALOUS - Deviates from normal user behavior"
                }
                anomaly_indicators.append(indicator)
        
        report = {
            "report_type": "Behavioral Anomaly Detection (ML Model)",
            "generated_at": self.timestamp,
            "model_used": "IsolationForest",
            "total_sessions_analyzed": len(curr),
            "anomalous_sessions": len(anomaly_indicators),
            "anomaly_rate_percent": round((len(anomaly_indicators) / len(curr)) * 100, 2) if len(curr) > 0 else 0,
            "high_risk_anomalies": len([x for x in anomaly_indicators if x['risk_level'] == 'HIGH']),
            "medium_risk_anomalies": len([x for x in anomaly_indicators if x['risk_level'] == 'MEDIUM']),
            "detections": anomaly_indicators
        }
        
        self.reports['behavioral_anomaly'] = report
        return report
    
    # ==============================
    def generate_data_integrity_report(self):
        """Detect data integrity and tracking issues"""
        df = self.data['input'].copy()
        
        issues = []
        
        for idx, row in df.iterrows():
            session_issues = {
                "session_id": row['session_id'],
                "visitor_id": row['visitor_id'],
                "severity": "INFO",
                "issues": []
            }
            
            # Check: Missing or invalid values
            if pd.isna(row['session_duration']):
                session_issues['issues'].append("missing_session_duration")
                session_issues['severity'] = "CRITICAL"
            
            if row['session_duration'] < 0:
                session_issues['issues'].append("invalid_negative_duration")
                session_issues['severity'] = "CRITICAL"
            
            if row['clicks'] < 0 or row['events_count'] < 0:
                session_issues['issues'].append("negative_metrics")
                session_issues['severity'] = "CRITICAL"
            
            # Check: Logical inconsistencies
            if row['clicks'] > row['events_count'] * 2:
                session_issues['issues'].append("clicks_exceed_events_ratio")
                session_issues['severity'] = "WARNING"
            
            if row['pages_viewed'] == 0 and row['session_duration'] > 60:
                session_issues['issues'].append("no_pages_long_duration")
                session_issues['severity'] = "WARNING"
            
            # Check: Tracking gaps
            if row['events_count'] == 0 and row['session_duration'] > 0:
                session_issues['issues'].append("no_events_recorded")
                session_issues['severity'] = "WARNING"
            
            # Check: Conversion tracking
            if row['converted'] == True and row['scroll_depth'] == 0:
                session_issues['issues'].append("conversion_no_engagement")
                session_issues['severity'] = "INFO"
            
            if session_issues['issues']:
                issues.append(session_issues)
        
        # Summary
        critical_issues = len([x for x in issues if x['severity'] == 'CRITICAL'])
        warning_issues = len([x for x in issues if x['severity'] == 'WARNING'])
        
        report = {
            "report_type": "Data Integrity & Tracking Issues Report",
            "generated_at": self.timestamp,
            "total_sessions_checked": len(df),
            "sessions_with_issues": len(issues),
            "critical_issues": critical_issues,
            "warning_issues": warning_issues,
            "data_quality_score": round(((len(df) - len(issues)) / len(df)) * 100, 2),
            "issues": issues
        }
        
        self.reports['data_integrity'] = report
        return report
    
    # ==============================
    # GENERATE ALL REPORTS
    # ==============================
    def generate_all_reports(self):
        """Generate all 6 reports (5 original + 1 new ML-based)"""
        print("📊 Generating Anomaly & Risk Detection Reports (Using ML Models)...")
        print()
        
        print("1️⃣  Traffic Spike/Drop Anomaly Report...")
        self.generate_traffic_spike_report()
        
        print("2️⃣  Behavioral Anomaly Detection (ML Model)...")
        self.generate_anomaly_detection_report()
        
        print("3️⃣  Fraud / Bot Traffic Detection (ML Model)...")
        self.generate_fraud_bot_report()
        
        print("4️⃣  Conversion Drop Alerts (ML Model)...")
        self.generate_conversion_drop_report()
        
        print("5️⃣  Revenue Leakage Detection (ML Model)...")
        self.generate_revenue_leakage_report()
        
        print("6️⃣  Data Integrity & Tracking Issues Report...")
        self.generate_data_integrity_report()
        
        return self.reports
    
    def save_reports(self, output_dir="../models"):
        """Save all reports to JSON files"""
        os.makedirs(output_dir, exist_ok=True)
        
        for report_name, report_data in self.reports.items():
            filename = f"{output_dir}/report_{report_name}.json"
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=4)
            print(f"✅ Saved: {filename}")
        
        # Save combined report
        combined = {
            "generated_at": self.timestamp,
            "total_reports": len(self.reports),
            "reports": self.reports
        }
        
        with open(f"{output_dir}/combined_report.json", 'w') as f:
            json.dump(combined, f, indent=4)
        print(f"✅ Saved: {output_dir}/combined_report.json")
    
    def print_summary(self):
        """Print summary of all reports"""
        print("\n" + "="*70)
        print("📈 ANOMALY & RISK DETECTION SUMMARY (ML-POWERED)".center(70))
        print("="*70)
        
        for report_name, report_data in self.reports.items():
            print(f"\n🔹 {report_data.get('report_type', 'Unknown')}")
            
            if 'model_used' in report_data:
                print(f"   🤖 Model: {report_data['model_used']}")
            
            if report_name == 'behavioral_anomaly':
                print(f"   • Total Sessions: {report_data['total_sessions_analyzed']}")
                print(f"   • Anomalous Sessions: {report_data['anomalous_sessions']}")
                print(f"   • Anomaly Rate: {report_data['anomaly_rate_percent']}%")
                print(f"   • High Risk: {report_data['high_risk_anomalies']}")
            
            elif report_name == 'fraud_bot':
                print(f"   • Total Sessions: {report_data['total_sessions_analyzed']}")
                print(f"   • Fraudulent Sessions: {report_data['fraudulent_sessions']}")
                print(f"   • Fraud Rate: {report_data['fraud_rate_percent']}%")
                print(f"   • High Confidence: {report_data['high_confidence_fraud']}")
            
            elif report_name == 'conversion_drop':
                print(f"   • Historical Conv Rate: {report_data['historical_conversion_rate']}%")
                print(f"   • Actual Conv Rate: {report_data['actual_current_conversion_rate']}%")
                print(f"   • Model Predicted Rate: {report_data['model_predicted_conversion_rate']}%")
                print(f"   • Actual Drop: {report_data['actual_conversion_drop_percent']}%")
                print(f"   • Model Alert: {report_data['model_alert_level']}")
            
            elif report_name == 'revenue_leakage':
                print(f"   • Total Sessions: {report_data['total_sessions']}")
                print(f"   • Leakage Risk Sessions: {report_data['leakage_risk_sessions']}")
                print(f"   • Critical Leakage: {report_data['critical_leakage_sessions']}")
                print(f"   • Medium Risk: {report_data['medium_leakage_sessions']}")
            
            elif report_name == 'data_integrity':
                print(f"   • Data Quality Score: {report_data['data_quality_score']}%")
                print(f"   • Critical Issues: {report_data['critical_issues']}")
                print(f"   • Warnings: {report_data['warning_issues']}")
            
            elif report_name == 'traffic_spike':
                print(f"   • Anomalies Detected: {len(report_data.get('metrics', {}))}")
        
        print("\n" + "="*60)

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    reporter = AnomalyReporter()
    reports = reporter.generate_all_reports()
    reporter.save_reports()
    reporter.print_summary()
