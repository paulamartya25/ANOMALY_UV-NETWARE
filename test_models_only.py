#!/usr/bin/env python3
"""
========================================
TEST MODELS ONLY - NO RETRAINING
========================================
This script uses ALREADY TRAINED models to make predictions.
Run this multiple times if you only want to test predictions.
Models are NOT retrained each time.
"""

import subprocess
import sys
import json
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(80)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

def print_section(title):
    """Print formatted section"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}> {title}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'─'*80}{Colors.ENDC}\n")

def run_script(script_name, description):
    """Run a Python script"""
    print(f"{Colors.YELLOW}[RUNNING] {description}...{Colors.ENDC}")
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
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.ENDC}")
        return False

def load_metrics(filepath, model_name):
    """Load and display metrics from JSON file"""
    try:
        with open(filepath, 'r') as f:
            metrics = json.load(f)
        
        print(f"\n{Colors.GREEN}[LOADED] {model_name} Metrics{Colors.ENDC}")
        print(f"{'─'*80}")
        print(f"Model: {metrics.get('model', 'N/A')}")
        print(f"Training Samples: {metrics.get('training_samples', 'N/A')}")
        print(f"Test Samples: {metrics.get('test_samples', 'N/A')}\n")
        
        print(f"{Colors.BOLD}Performance Metrics:{Colors.ENDC}")
        print(f"  • Accuracy:  {Colors.GREEN}{metrics.get('accuracy', 0):.4f} ({metrics.get('accuracy', 0)*100:.2f}%){Colors.ENDC}")
        print(f"  • Precision: {Colors.GREEN}{metrics.get('precision', 0):.4f}{Colors.ENDC}")
        print(f"  • Recall:    {Colors.GREEN}{metrics.get('recall', 0):.4f}{Colors.ENDC}")
        print(f"  • F1 Score:  {Colors.GREEN}{metrics.get('f1_score', 0):.4f}{Colors.ENDC}")
        
        return metrics
    except FileNotFoundError:
        print(f"{Colors.RED}[ERROR] Metrics file not found: {filepath}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[HINT] Run train_models_once.py first to train models{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.ENDC}")
        return None

def main():
    print_header("TEST MODELS ONLY - USING SAVED MODELS (NO RETRAINING)")
    
    start_time = datetime.now()
    print(f"{Colors.CYAN}Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.YELLOW}Note: Models are NOT retrained. Using existing saved models.{Colors.ENDC}\n")
    
    # Check if models exist
    print_section("Checking for Saved Models")
    
    fraud_metrics = load_metrics("models/fraud_metrics.json", "FRAUD DETECTION")
    print("\n")
    conversion_metrics = load_metrics("models/conversion_metrics.json", "CONVERSION PREDICTION")
    
    if not fraud_metrics or not conversion_metrics:
        print(f"\n{Colors.RED}[ERROR] Models not found!{Colors.ENDC}")
        print(f"{Colors.YELLOW}Run:  python train_models_once.py{Colors.ENDC}\n")
        return
    
    # Run Predictions
    print_section("Running Predictions on Test Data")
    
    print(f"{Colors.BOLD}This will use the trained models to make predictions...{Colors.ENDC}\n")
    
    # Fraud Predictions
    print_header("Step 1/2: Fraud Detection Predictions")
    run_script("run_fraud.py", "Testing Fraud Detection Model")
    
    # Conversion Predictions
    print_header("Step 2/2: Conversion Predictions")
    run_script("test_conversion.py", "Testing Conversion Prediction Model")
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_section("PREDICTION SUMMARY")
    
    print(f"{Colors.BOLD}{Colors.CYAN}FRAUD DETECTION MODEL{Colors.ENDC}")
    if fraud_metrics:
        print(f"  └─ Accuracy: {Colors.GREEN}{fraud_metrics.get('accuracy', 0):.4f}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}CONVERSION PREDICTION MODEL{Colors.ENDC}")
    if conversion_metrics:
        print(f"  └─ Accuracy: {Colors.GREEN}{conversion_metrics.get('accuracy', 0):.4f}{Colors.ENDC}")
    
    print_header("TESTING COMPLETE")
    print(f"{Colors.GREEN}Duration: {duration:.2f} seconds{Colors.ENDC}\n")
    print(f"{Colors.BOLD}{Colors.YELLOW}To retrain models: python train_models_once.py{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
