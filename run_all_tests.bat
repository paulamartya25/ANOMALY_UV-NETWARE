@echo off
REM ============================================
REM MASTER TEST SCRIPT - Run All Models
REM ============================================
REM This batch file runs all models in sequence
REM and displays accuracy metrics

echo.
echo ============================================
echo   COMPLETE MODEL TRAINING & TESTING PIPELINE
echo ============================================
echo.
echo Starting model tests...
echo.

REM Run all tests
python run_all_tests.py

pause
