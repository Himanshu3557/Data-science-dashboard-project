import os
from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__, template_folder="templates", static_folder="static")

# ==========================
# LOAD & PREPROCESS DATA
# ==========================

def load_and_preprocess_data():

    dataset_path = os.path.join(
        app.root_path,
        "heart_patient_dataset.xlsx"
    )

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    df = pd.read_excel(dataset_path)

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove missing values
    df = df.dropna()

    # Clean string columns
    string_columns = df.select_dtypes(include=["object"]).columns

    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    return df


# ==========================
# SUMMARY STATISTICS
# ==========================

def calculate_summary_stats(df):

    numeric_cols = df.select_dtypes(
        include=[np.number]
    ).columns

    if df.empty:
        return {
            metric: {
                col: 0 for col in numeric_cols
            }
            for metric in [
                "mean",
                "median",
                "max",
                "min",
                "std"
            ]
        }

    summary = {
        "mean": df[numeric_cols].mean().round(2).to_dict(),
        "median": df[numeric_cols].median().round(2).to_dict(),
        "max": df[numeric_cols].max().round(2).to_dict(),
        "min": df[numeric_cols].min().round(2).to_dict(),
        "std": df[numeric_cols].std().round(2).to_dict()
    }

    return summary


# ==========================
# KPI CALCULATIONS
# ==========================

def calculate_kpis(df):
    if df.empty:
        return {
            "total_patients": 0,
            "avg_age": 0,
            "avg_bmi": 0,
            "avg_cholesterol": 0,
            "avg_systolic_bp": 0,
            "avg_blood_sugar": 0
        }

    def safe_numeric_mean(series):
        nums = pd.to_numeric(series, errors="coerce")
        m = nums.mean()
        return 0 if pd.isna(m) else round(m, 1)

    return {
        "total_patients": len(df),
        "avg_age": safe_numeric_mean(df.get("Age", pd.Series(dtype="float"))),
        "avg_bmi": safe_numeric_mean(df.get("BMI", pd.Series(dtype="float"))),
        "avg_cholesterol": safe_numeric_mean(df.get("Cholesterol_Level", pd.Series(dtype="float"))),
        "avg_systolic_bp": safe_numeric_mean(df.get("Systolic_BP", pd.Series(dtype="float"))),
        "avg_blood_sugar": safe_numeric_mean(df.get("Blood_Sugar", pd.Series(dtype="float")))
    }


# ==========================
# HOME PAGE
# ==========================

@app.route("/")
def index():

    df = load_and_preprocess_data()

    # ------------------
    # FILTERS
    # ------------------

    gender_filter = request.args.get(
        "gender", ""
    )

    age_min = request.args.get(
        "age_min", ""
    )

    age_max = request.args.get(
        "age_max", ""
    )

    smoking_filter = request.args.get(
        "smoking_status", ""
    )

    chest_pain_filter = request.args.get(
        "chest_pain_type", ""
    )

    diagnosis_filter = request.args.get(
        "clinical_diagnosis", ""
    )

    risk_filter = request.args.get(
        "cardiac_risk_level", ""
    )

    # ------------------
    # APPLY FILTERS
    # ------------------

    filtered_df = df.copy()

    if gender_filter:
        filtered_df = filtered_df[
            filtered_df["Gender"] == gender_filter
        ]

    if age_min:
        filtered_df = filtered_df[
            filtered_df["Age"] >= int(age_min)
        ]

    if age_max:
        filtered_df = filtered_df[
            filtered_df["Age"] <= int(age_max)
        ]

    if smoking_filter:
        filtered_df = filtered_df[
            filtered_df["Smoking_Status"]
            == smoking_filter
        ]

    if chest_pain_filter:
        filtered_df = filtered_df[
            filtered_df["Chest_Pain_Type"]
            == chest_pain_filter
        ]

    if diagnosis_filter:
        filtered_df = filtered_df[
            filtered_df["Clinical_Diagnosis"]
            == diagnosis_filter
        ]

    if risk_filter:
        filtered_df = filtered_df[
            filtered_df["Cardiac_Risk_Level"]
            == risk_filter
        ]

    # ------------------
    # KPIs & SUMMARY
    # ------------------

    kpis = calculate_kpis(filtered_df)

    summary_stats = calculate_summary_stats(
        filtered_df
    )

    top_records = filtered_df.head(
        20
    ).to_dict("records")

    # ------------------
    # DROPDOWNS
    # ------------------

    genders = sorted(
        df["Gender"].dropna().unique()
    )

    smoking_statuses = sorted(
        df["Smoking_Status"].dropna().unique()
    )

    chest_pain_types = sorted(
        df["Chest_Pain_Type"].dropna().unique()
    )

    diagnoses = sorted(
        df["Clinical_Diagnosis"].dropna().unique()
    )

    risk_levels = sorted(
        df["Cardiac_Risk_Level"].dropna().unique()
    )

    # ------------------
    # RENDER PAGE
    # ------------------

    return render_template(
        "index.html",

        kpis=kpis,

        summary_stats=summary_stats,

        top_records=top_records,

        genders=genders,

        smoking_statuses=smoking_statuses,

        chest_pain_types=chest_pain_types,

        diagnoses=diagnoses,

        risk_levels=risk_levels,

        filters={
            "gender": gender_filter,
            "age_min": age_min,
            "age_max": age_max,
            "smoking_status": smoking_filter,
            "chest_pain_type": chest_pain_filter,
            "clinical_diagnosis": diagnosis_filter,
            "cardiac_risk_level": risk_filter
        }
    )


# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5001)
    )

    app.run(
        debug=True,
        host="0.0.0.0",
        port=port
    )