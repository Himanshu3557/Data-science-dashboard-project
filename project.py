import os
import numpy as np
import pandas as pd


def generate_heart_patient_dataset(num_records=10000):
    # Set random seed for reproducibility
    np.random.seed(42)

    # Generate Patient IDs
    patient_ids = [f"P{i:06d}" for i in range(1, num_records + 1)]

    # Age (Skewed older for cardiac patients: 30-90)
    age = np.random.randint(30, 91, num_records)

    # Gender
    gender = np.random.choice(
        ["Male", "Female", "Other"], num_records, p=[0.52, 0.46, 0.02]
    )

    # Core Vitals
    resting_heart_rate = np.random.randint(50, 111, num_records)
    max_heart_rate_achieved = (
        (220 - age) - np.random.randint(10, 40, num_records)
    ).astype(int)

    # Blood Pressure (Systolic & Diastolic)
    systolic_bp = np.random.randint(90, 191, num_records)
    # Ensure diastolic is naturally lower than systolic
    diastolic_bp = (systolic_bp * 0.65 + np.random.randint(-10, 15, num_records)).astype(
        int
    )

    # Lifestyle & Metabolic Factors
    height_cm = np.random.uniform(145, 200, num_records).round(1)
    weight_kg = np.random.uniform(40, 130, num_records).round(1)
    bmi = (weight_kg / (height_cm / 100) ** 2).round(1)

    smoking_status = np.random.choice(
        ["Never", "Former", "Current"], num_records, p=[0.5, 0.3, 0.2]
    )
    cholesterol_level = np.random.choice(
        ["Normal", "Borderline", "High"], num_records, p=[0.4, 0.3, 0.3]
    )
    blood_sugar = np.random.choice(
        ["Normal", "Prediabetes", "Diabetes"], num_records, p=[0.5, 0.3, 0.2]
    )

    # Cardiac Specific Symptoms & History
    chest_pain_type = np.random.choice(
        [
            "Typical Angina",
            "Atypical Angina",
            "Non-Anginal Pain",
            "Asymptomatic",
        ],
        num_records,
        p=[0.2, 0.2, 0.3, 0.3],
    )
    ekg_results = np.random.choice(
        ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"],
        num_records,
        p=[0.5, 0.3, 0.2],
    )
    history_of_mi = np.random.choice(
        ["Yes", "No"], num_records, p=[0.15, 0.85]
    )  # Myocardial Infarction (Heart Attack)
    family_history_cardiac = np.random.choice(
        ["Yes", "No"], num_records, p=[0.3, 0.7]
    )

    # Logic to Determine Heart Condition Severity (Risk Engine)
    def diagnose_patient(row):
        severity_points = 0

        # Age and Family History factors
        if row["Age"] > 60:
            severity_points += 1
        if row["Family_History_Cardiac"] == "Yes":
            severity_points += 1

        # Vital signs factors
        if row["Systolic_BP"] >= 140 or row["Diastolic_BP"] >= 90:
            severity_points += 2
        if row["Cholesterol_Level"] == "High":
            severity_points += 1
        if row["Blood_Sugar"] == "Diabetes":
            severity_points += 1

        # Clinical presentation factors
        if row["Chest_Pain_Type"] in ["Typical Angina", "Atypical Angina"]:
            severity_points += 2
        if row["EKG_Results"] != "Normal":
            severity_points += 2
        if row["History_of_MI"] == "Yes":
            severity_points += 3

        # Diagnosis assignment based on accumulated clinical points
        if severity_points >= 8:
            return "Coronary Artery Disease (CAD)", "High"
        elif severity_points >= 5:
            return "Hypertensive Heart Disease", "Medium"
        elif severity_points >= 3:
            return "Mild Arrhythmia / At Risk", "Low"
        else:
            return "Healthy / No Significant Risk", "Low"

    # Temporary DataFrame construction to evaluate the row-by-row function
    temp_df = pd.DataFrame(
        {
            "Age": age,
            "Family_History_Cardiac": family_history_cardiac,
            "Systolic_BP": systolic_bp,
            "Diastolic_BP": diastolic_bp,
            "Cholesterol_Level": cholesterol_level,
            "Blood_Sugar": blood_sugar,
            "Chest_Pain_Type": chest_pain_type,
            "EKG_Results": ekg_results,
            "History_of_MI": history_of_mi,
        }
    )

    # Apply medical rules engine
    diagnoses = temp_df.apply(diagnose_patient, axis=1)
    condition_labels = [d[0] for d in diagnoses]
    risk_labels = [d[1] for d in diagnoses]

    # Final Comprehensive DataFrame Generation
    df = pd.DataFrame(
        {
            "Patient_ID": patient_ids,
            "Age": age,
            "Gender": gender,
            "Height_cm": height_cm,
            "Weight_kg": weight_kg,
            "BMI": bmi,
            "Systolic_BP": systolic_bp,
            "Diastolic_BP": diastolic_bp,
            "Resting_Heart_Rate": resting_heart_rate,
            "Max_Heart_Rate_Achieved": max_heart_rate_achieved,
            "Cholesterol_Level": cholesterol_level,
            "Blood_Sugar": blood_sugar,
            "Smoking_Status": smoking_status,
            "Chest_Pain_Type": chest_pain_type,
            "EKG_Results": ekg_results,
            "History_of_MI": history_of_mi,
            "Family_History_Cardiac": family_history_cardiac,
            "Clinical_Diagnosis": condition_labels,
            "Cardiac_Risk_Level": risk_labels,
        }
    )

    return df


if __name__ == "__main__":
    print("Generating heart patient dataset...")
    dataset = generate_heart_patient_dataset(10000)
    print("Dataset generated successfully!")

    print("\nFirst 5 Records Preview:")
    print(dataset.head().to_string())

    print("\nSaving dataset to heart_patient_dataset.xlsx...")
    os.makedirs("dataset", exist_ok=True)
    dataset.to_excel("dataset/heart_patient_dataset.xlsx", index=False)
    print("Dataset saved successfully inside the 'dataset' directory!")