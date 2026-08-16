import numpy as np
from typing import Dict, Any, List

class ModelEvaluator:
    """
    Data Science Model Evaluation Engine.
    Computes Accuracy, Precision, Recall, F1 Score, Confusion Matrix, and Class-wise Metrics.
    """
    CLASSES = [
        "tomato_early_blight",
        "tomato_late_blight",
        "tomato_yellow_leaf_curl",
        "potato_late_blight",
        "corn_common_rust",
        "healthy_leaf"
    ]

    @classmethod
    def compute_metrics(cls, y_true: List[int], y_pred: List[int]) -> Dict[str, Any]:
        """
        Computes formal classification metrics without fabricating data.
        """
        if not y_true or len(y_true) != len(y_pred):
            return {
                "error": "y_true and y_pred must be non-empty lists of identical length"
            }

        y_t = np.array(y_true)
        y_p = np.array(y_pred)

        correct = np.sum(y_t == y_p)
        total = len(y_t)
        accuracy = round(float(correct / total), 4)

        # Build confusion matrix
        num_classes = len(cls.CLASSES)
        cm = np.zeros((num_classes, num_classes), dtype=int)
        for t, p in zip(y_t, y_p):
            if 0 <= t < num_classes and 0 <= p < num_classes:
                cm[t][p] += 1

        class_metrics = {}
        for i, cname in enumerate(cls.CLASSES):
            tp = cm[i][i]
            fp = np.sum(cm[:, i]) - tp
            fn = np.sum(cm[i, :]) - tp
            
            precision = round(float(tp / (tp + fp)), 4) if (tp + fp) > 0 else 0.0
            recall = round(float(tp / (tp + fn)), 4) if (tp + fn) > 0 else 0.0
            f1 = round(float(2 * precision * recall / (precision + recall)), 4) if (precision + recall) > 0 else 0.0

            class_metrics[cname] = {
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "support": int(np.sum(cm[i, :]))
            }

        macro_f1 = round(float(np.mean([m["f1_score"] for m in class_metrics.values()])), 4)

        return {
            "accuracy": accuracy,
            "macro_f1_score": macro_f1,
            "confusion_matrix": cm.tolist(),
            "class_metrics": class_metrics,
            "total_eval_samples": total
        }

if __name__ == "__main__":
    # Test sample evaluation calculation
    y_true_sample = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3]
    y_pred_sample = [0, 1, 2, 3, 4, 5, 0, 1, 1, 3]
    res = ModelEvaluator.compute_metrics(y_true_sample, y_pred_sample)
    print("Sample Model Evaluation Results:", res)
