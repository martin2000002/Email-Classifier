import json
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
import numpy as np
from tqdm import tqdm
from itertools import product
import argparse
DATA_PATH = Path("../../data/dataset.jsonl")
MODEL_PATH = Path("model.joblib")

def load_data():
    """Load dataset from JSONL file (email, label)."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH.resolve()}. Generate data first."
        )

    texts = []
    labels = []

    print(f"Loading data from {DATA_PATH}...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                texts.append(data["email"])
                labels.append(data["label"])
            except json.JSONDecodeError:
                continue

    return texts, labels

def train(no_plot: bool = False):
    print("=== Starting Model Training (manual CV + heatmap) ===")
    try:
        X, y = load_data()
    except Exception as e:
        print(f"Error: {e}")
        return

    if len(X) < 10:
        print("Error: Too few samples to train. Generate more examples first.")
        return

    print(f"Total samples: {len(X)}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    def make_pipeline(max_features, ngram_range, C):
        return Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=max_features, ngram_range=ngram_range)),
            ("clf", LogisticRegression(class_weight="balanced", random_state=42, max_iter=1000, C=C)),
        ])
    max_features_list = [15000, 20000, 25000]
    ngram_ranges = [(1,2)]
    C_values = [40, 50, 60]

    results = []

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    print("\nBeginning cross-validation over parameter combinations...")
    combo_iter = list(product(max_features_list, ngram_ranges, C_values))
    for mf, ng, C in tqdm(combo_iter, desc="Hyperparam combos", unit="combo"):
        fold_scores = []
        for train_idx, val_idx in tqdm(list(skf.split(X_train, y_train)), desc=f"CV folds mf={mf} ng={ng} C={C}", leave=False, unit="fold"):
            X_tr = [X_train[i] for i in train_idx]
            y_tr = [y_train[i] for i in train_idx]
            X_val = [X_train[i] for i in val_idx]
            y_val = [y_train[i] for i in val_idx]

            pipeline = make_pipeline(mf, ng, C)
            pipeline.fit(X_tr, y_tr)
            score = pipeline.score(X_val, y_val)
            fold_scores.append(score)

        mean_score = float(np.mean(fold_scores))
        std_score = float(np.std(fold_scores))
        results.append({
            "max_features": mf,
            "ngram_range": ng,
            "C": C,
            "mean_score": mean_score,
            "std_score": std_score,
        })
    try:
        subset = [r for r in results if r["ngram_range"] == (1,2)]
        matrix = np.zeros((len(max_features_list), len(C_values)))
        for i_mf, mf in enumerate(max_features_list):
            for j_C, C in enumerate(C_values):
                match = [r for r in subset if r["max_features"] == mf and r["C"] == C]
                matrix[i_mf, j_C] = match[0]["mean_score"] if match else np.nan
        plt.figure(figsize=(6,5))
        im = plt.imshow(matrix, aspect="auto", cmap="viridis")
        plt.title("Mean CV Score Heatmap (ngram_range=(1,2))")
        plt.xlabel("C")
        plt.ylabel("max_features")
        plt.xticks(range(len(C_values)), C_values)
        plt.yticks(range(len(max_features_list)), max_features_list)
        for i in range(len(max_features_list)):
            for j in range(len(C_values)):
                val = matrix[i, j]
                if not np.isnan(val):
                    plt.text(j, i, f"{val:.3f}", ha="center", va="center", color="white" if val < (np.nanmax(matrix) * 0.7) else "black")
        plt.colorbar(im, pad=0.02)
        plt.tight_layout()
        if not no_plot:
            print("Displaying heatmaps (close window to continue)...")
            plt.show()
    except Exception as e:
        print(f"Could not generate heatmap: {e}")
    best = max(results, key=lambda r: r["mean_score"])
    print(f"\nBest combination (CV mean): mf={best['max_features']}, ng={best['ngram_range']}, C={best['C']} -> {best['mean_score']:.4f}")
    final_pipeline = make_pipeline(best['max_features'], best['ngram_range'], best['C'])
    final_pipeline.fit(X_train, y_train)
    print("\nEvaluating best model on Test Set...")
    y_pred = final_pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(f"Saving best model to {MODEL_PATH}...")
    joblib.dump(final_pipeline, MODEL_PATH)
    print("=== Training Completed Successfully ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train email classifier")
    parser.add_argument("--no-plot", action="store_true", help="Disable matplotlib popup (no plt.show)")
    args = parser.parse_args()
    train(no_plot=args.no_plot)
