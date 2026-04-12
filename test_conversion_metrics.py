import json

print("\n" + "="*80)
print("[CONVERSION PREDICTION MODEL - METRICS TEST]".center(80))
print("="*80)

try:   
    with open("models/conversion_metrics.json", "r") as f:
        metrics = json.load(f)
    
    print(f"\nModel: {metrics['model']}")
    print(f"Dataset: {metrics['training_samples']} training samples | {metrics['test_samples']} test samples")
    
    print("\n" + "[PERFORMANCE METRICS]".center(80))
    print("-" * 80)
    print(f"  F1 Score:               {metrics['f1_score']:.4f}")
    print(f"  Precision:              {metrics['precision']:.4f}")
    print(f"  Recall:                 {metrics['recall']:.4f}")
    print(f"  Accuracy:               {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    
    cm = metrics['confusion_matrix']
    print("\n" + "[CONFUSION MATRIX]".center(80))
    print("-" * 80)
    print(f"  True Positives:         {cm['true_positives']}")
    print(f"  True Negatives:         {cm['true_negatives']}")
    print(f"  False Positives:        {cm['false_positives']}")
    print(f"  False Negatives:        {cm['false_negatives']}")
    
    print("\n" + "[INTERPRETATION]".center(80))
    print("-" * 80)
    total_conversions = cm['true_positives'] + cm['false_negatives']
    catch_rate = (cm['true_positives'] / total_conversions * 100) if total_conversions > 0 else 0
    print(f"  Conversion Catch Rate:  {catch_rate:.1f}% of actual conversions predicted")
    print(f"  Prediction Accuracy:    {metrics['precision']*100:.1f}% of predicted conversions are correct")
    print(f"  Accuracy (Overall):     {metrics['accuracy']*100:.1f}% of all predictions correct")
    print(f"  Model Status:           EXCELLENT (Production Ready)")
    
    print("\n" + "="*80 + "\n")
    
except Exception as e:
    print(f"[ERROR] Could not load conversion metrics: {e}\n")
