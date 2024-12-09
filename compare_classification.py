import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, classification_report
import argparse
import os

def load_predictions(file_path):
    """Load prediction data from file."""
    data = pd.read_csv(file_path, sep="\t", header=None, names=["Region", "Label", "Score"])
    return data

def plot_roc_curve(y_true, decision_scores, label, ax):
    """Plot ROC curve using decision scores."""
    fpr, tpr, _ = roc_curve(y_true, decision_scores)
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, label=f'{label} (AUC = {roc_auc:.2f})')

def main(args):
    # Load predictions
    skipper = load_predictions(args.rbp + ".skipper.predictions")
    clipper = load_predictions(args.rbp + ".clipper.predictions")
    
    # Extract true labels and decision scores
    y_true_skipper = skipper["Label"]
    decision_scores_skipper = skipper["Score"]
    y_true_clipper = clipper["Label"]
    decision_scores_clipper = clipper["Score"]
    
    # Generate classification reports
    threshold = 0  # Default threshold for SVM decision scores
    report_skipper = classification_report(y_true_skipper, (decision_scores_skipper > threshold).astype(int))
    report_clipper = classification_report(y_true_clipper, (decision_scores_clipper > threshold).astype(int))
    
    # Save classification reports
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, f"{args.rbp}_classification_report.txt"), "w") as f:
        f.write("Skipper Classification Report:\n")
        f.write(report_skipper)
        f.write("\n\nClipper Classification Report:\n")
        f.write(report_clipper)
    
    # Plot ROC curves
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_roc_curve(y_true_skipper, decision_scores_skipper, "Skipper", ax)
    plot_roc_curve(y_true_clipper, decision_scores_clipper, "Clipper", ax)
    ax.plot([0, 1], [0, 1], 'k--', lw=2)
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curve Comparison')
    ax.legend(loc="lower right")
    plt.savefig(os.path.join(output_dir, f"{args.rbp}_roc_curve.png"))
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare classification performance of Skipper and Clipper predictions.")
    parser.add_argument("-r", "--rbp", required=True, help="RBP identifier (used as prefix for prediction files).")
    parser.add_argument("-o", "--output", required=True, help="Output directory for results.")
    args = parser.parse_args()
    main(args)

