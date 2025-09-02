# Offline script (trains and saves model.pkl)
import pandas as pd
import glob
import re 
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib

# -------------------------------
# Feature Extraction
# -------------------------------
def extract_features_from_column(series: pd.Series):
    data = series.astype(str).fillna("")
    return {
        "unique_ratio": series.nunique() / len(series),
        "avg_len": data.str.len().mean(),
        "pct_numeric": data.str.match(r'^\d+(\.\d+)?$').mean(),
        "pct_date": data.str.match(r'^\d{4}-\d{2}-\d{2}$').mean(),
        "starts_with_digit": data.str.match(r'^\d').mean(),
        "contains_text": data.str.match(r'[A-Za-z]').mean()
    }

# -------------------------------
# Build Training Dataset
# -------------------------------
X, y = [], []

for labeled_file in glob.glob("data/*_labeled.csv"):
    obfuscated_file = labeled_file.replace("_labeled", "_obfuscated")

    df_labeled = pd.read_csv(labeled_file)
    df_obf = pd.read_csv(obfuscated_file)

    for i, col in enumerate(df_obf.columns):
        feats = extract_features_from_column(df_obf[col])
        X.append(list(feats.values()))
        y.append(df_labeled.columns[i]) # true schema name 

feature_names = list(feats.keys())
X = pd.DataFrame(X, columns=feature_names)
y = pd.Series(y)

# -------------------------------
# Train Classifier
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(eval_metric="mlogloss", use_label_encoder=False)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump((model, feature_names), "column_predictor.pkl")

