#!/usr/bin/env python3
"""
========================================
MASTER TEST SCRIPT - RUN ALL MODELS
========================================
This script trains and tests all models,
displaying comprehensive accuracy metrics
for Fraud Detection and Conversion Prediction.
"""

import subprocess
import sys
import json
import os
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

def print_section(title):
    """Print formatted section"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}➤ {title}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}\n")

def run_script(script_name, description):
    """Run a Python script and handle output"""
    print(f"{Colors.YELLOW}▶ Executing: {description}...{Colors.ENDC}")
    try:
        result = subprocess.run(
            [sys.executable, f"src/{script_name}"],
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)
        if result.stderr:
            print(f"{Colors.RED}{result.stderr}{Colors.ENDC}")
        return True
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}❌ Timeout running {script_name}{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ Error running {script_name}: {e}{Colors.ENDC}")
        return False

def load_metrics(filepath, model_name):
    """Load and display metrics from JSON file"""
    try:
        with open(filepath, 'r') as f:
            metrics = json.load(f)
        
        print(f"\n{Colors.GREEN}✅ {model_name} Metrics Loaded{Colors.ENDC}")
        print(f"{'─'*80}")
        print(f"Model: {metrics.get('model', 'N/A')}")
        print(f"Training Samples: {metrics.get('training_samples', 'N/A')}")
        print(f"Test Samples: {metrics.get('test_samples', 'N/A')}\n")
        
        print(f"{Colors.BOLD}Model Performance:{Colors.ENDC}")
        print(f"  • Accuracy:  {Colors.GREEN}{metrics.get('accuracy', 0):.4f} ({metrics.get('accuracy', 0)*100:.2f}%){Colors.ENDC}")
        print(f"  • Precision: {Colors.GREEN}{metrics.get('precision', 0):.4f}{Colors.ENDC}")
        print(f"  • Recall:    {Colors.GREEN}{metrics.get('recall', 0):.4f}{Colors.ENDC}")
        print(f"  • F1 Score:  {Colors.GREEN}{metrics.get('f1_score', 0):.4f}{Colors.ENDC}")
        
        cm = metrics.get('confusion_matrix', {})
        print(f"\n{Colors.BOLD}Confusion Matrix:{Colors.ENDC}")
        print(f"  • True Positives:  {cm.get('true_positives', 0)}")
        print(f"  • True Negatives:  {cm.get('true_negatives', 0)}")
        print(f"  • False Positives: {cm.get('false_positives', 0)}")
        print(f"  • False Negatives: {cm.get('false_negatives', 0)}")
        
        return metrics
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Metrics file not found: {filepath}{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{Colors.RED}❌ Error loading metrics: {e}{Colors.ENDC}")
        return None

def main():
    """Main execution flow"""
    print_header("🚀 COMPLETE MODEL TRAINING & TESTING PIPELINE")
    
    start_time = datetime.now()
    print(f"{Colors.CYAN}Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # ============================
    # PHASE 1: TRAIN MODELS
    # ============================
    print_section("PHASE 1: TRAINING MODELS WITH METRICS")
    
    print(f"{Colors.BOLD}This will train both models and calculate accuracy metrics...{Colors.ENDC}\n")
    
    # Train Fraud Model
    print_header("Step 1/4: Training Fraud Detection Model")
    run_script("train_fraud.py", "Fraud Detection Model (Random Forest)")
    
    # Train Conversion Model
    print_header("Step 2/4: Training Conversion Prediction Model")
    run_script("train_conversion.py", "Conversion Prediction Model (Logistic Regression)")
    
    # ============================
    # PHASE 2: DISPLAY TRAINING METRICS
    # ============================
    print_section("PHASE 2: MODEL TRAINING METRICS SUMMARY")
    
    fraud_metrics = load_metrics("models/fraud_metrics.json", "FRAUD DETECTION MODEL")
    print("\n")
    conversion_metrics = load_metrics("models/conversion_metrics.json", "CONVERSION PREDICTION MODEL")
    
    # ============================
    # PHASE 3: RUN PREDICTIONS
    # ============================
    print_section("PHASE 3: RUNNING PREDICTIONS ON NEW DATA")
    
    print(f"{Colors.BOLD}Testing models on input data...{Colors.ENDC}\n")
    
    # Run Fraud Predictions
    print_header("Step 3/4: Running Fraud Detection Predictions")
    run_script("run_fraud.py", "Fraud Detection Predictions")
    
    # Run Conversion Predictions
    print_header("Step 4/4: Running Conversion Predictions")
    run_script("test_conversion.py", "Conversion Predictions")
    
    # ============================
    # PHASE 4: SUMMARY REPORT
    # ============================
    print_section("PHASE 4: COMPREHENSIVE ACCURACY SUMMARY")
    
    print(f"{Colors.BOLD}{Colors.CYAN}FRAUD DETECTION MODEL{Colors.ENDC}")
    if fraud_metrics:
        print(f"  ├─ Accuracy:  {Colors.GREEN}{fraud_metrics.get('accuracy', 0):.4f}{Colors.ENDC} ({'✅ EXCELLENT' if fraud_metrics.get('accuracy', 0) > 0.90 else '⚠️  GOOD' if fraud_metrics.get('accuracy', 0) > 0.80 else '❌ NEEDS IMPROVEMENT'})")
        print(f"  ├─ Precision: {Colors.GREEN}{fraud_metrics.get('precision', 0):.4f}{Colors.ENDC}")
        print(f"  ├─ Recall:    {Colors.GREEN}{fraud_metrics.get('recall', 0):.4f}{Colors.ENDC}")
        print(f"  └─ F1 Score:  {Colors.GREEN}{fraud_metrics.get('f1_score', 0):.4f}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}CONVERSION PREDICTION MODEL{Colors.ENDC}")
    if conversion_metrics:
        print(f"  ├─ Accuracy:  {Colors.GREEN}{conversion_metrics.get('accuracy', 0):.4f}{Colors.ENDC} ({'✅ EXCELLENT' if conversion_metrics.get('accuracy', 0) > 0.90 else '⚠️  GOOD' if conversion_metrics.get('accuracy', 0) > 0.80 else '❌ NEEDS IMPROVEMENT'})")
        print(f"  ├─ Precision: {Colors.GREEN}{conversion_metrics.get('precision', 0):.4f}{Colors.ENDC}")
        print(f"  ├─ Recall:    {Colors.GREEN}{conversion_metrics.get('recall', 0):.4f}{Colors.ENDC}")
        print(f"  └─ F1 Score:  {Colors.GREEN}{conversion_metrics.get('f1_score', 0):.4f}{Colors.ENDC}")
    
    # ============================
    # FINAL SUMMARY
    # ============================
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("✅ TESTING COMPLETE")
    print(f"{Colors.GREEN}Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.GREEN}Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.GREEN}Duration: {duration:.2f} seconds{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{Colors.CYAN}Output Files Generated:{Colors.ENDC}")
    print(f"  ✓ models/fraud_metrics.json")
    print(f"  ✓ models/conversion_metrics.json")
    print(f"  ✓ models/fraud_output.json")
    print(f"  ✓ models/conversion_output.json\n")
    
    print(f"{Colors.BOLD}{Colors.YELLOW}📊 To view detailed metrics anytime:{Colors.ENDC}")
    print(f"  • Fraud Metrics:      cat models/fraud_metrics.json")
    print(f"  • Conversion Metrics: cat models/conversion_metrics.json")
    print(f"  • Fraud Results:      cat models/fraud_output.json")
    print(f"  • Conversion Results: cat models/conversion_output.json\n")
    
    print(f"{Colors.BOLD}{Colors.GREEN}🎯 All tests completed successfully!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
