"""
Reads synthetic paired CSVs (same as original training)
Reads feadback.jsonl
Builds a combined dataset features + labels
Retrains the model and saves new column predictor.pkl
"""

import pandas as pd
import glob, json
from xgboost import XGBClassifier
from  sklearn.model_selection import train_test_split
import joblib

FEEDBACK_FILE = "feedback.jsonl"
MODEL_FILE = "app/column_predictor.pkl"

X, y = []



# ------------------------------
# Feature Extraction (Same as before)
# ------------------------------

def extract_features_from_column(series: pd.Series):
    data = series.astype(str).fillna("")
    return {
        "unique_ratio": series.nunique() / len(series),
        "avg_len": data.str.len().mean(),
        "pct_numeric": data.str.match(r'^\d+(\.\d+)?$').mean(),
        "pct_date": data.str.match(r'^\d{4}-\d{2}-\d{2}$'),
        "starts_with_digit": data.str.match(r'^\d').mean(),
        "contains_text": data.str.match(r'[A-Za-z]').mean()
    }

# ----------------------------
# Build Dataset from Synthetic Data
# ----------------------------
for labeled_file in glob.glob("training/data/*_labeled.csv"):
    obfuscated_file = labeled_file.replace("_labeled", "_obfuscated")

    df_labeled = pd.read_csv(labeled_file)
    df_obf = pd.read_csv(obfuscated_file)

    for i, col in enumerate(df_obf.columns):
        feats = extract_features_from_column(df_obf[col])
        X.append(list(feats.values()))
        y.append(df_labeled.columns[i])  # true schema name

feature_names = list(feats.keys())

# -------------------------------
# Add Feedback Data (if exists)
# -------------------------------
try:
    with open(FEEDBACK_FILE, "r") as f:
        for line in f:
            item = json.loads(line)
            sample_series = pd.Series(item["sample_values"])
            feats = extract_features_from_column(sample_series)
            X.append(list(feats.values()))
            y.append(item["corrected"])
    print("✅ Loaded feedback corrections")
except FileNotFoundError:
    print("⚠️ No feedback file found, training only on synthetic data")

# -------------------------------
# Train New Model
# -------------------------------
X = pd.DataFrame(X, columns=feature_names)
y = pd.Series(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(eval_metric="mlogloss", use_label_encoder=False)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

# Save updated model
joblib.dump((model, feature_names), MODEL_FILE)
print(f"✅ New model saved to {MODEL_FILE}")
