import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Load Dataset
def load_data():
    df = pd.read_excel("heart_patient_dataset.xlsx")

    df = df.drop_duplicates()
    df = df.dropna()

    return df


# Generate Graphs
def generate_all_graphs(df):

    sns.set_style("whitegrid")

    os.makedirs("graphs", exist_ok=True)

    # 1. Gender Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Gender")
    plt.title("Gender Distribution")
    plt.savefig("graphs/gender_distribution.png")
    plt.close()

    # 2. Age Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Age"], bins=20, kde=True)
    plt.title("Age Distribution")
    plt.savefig("graphs/age_distribution.png")
    plt.close()

    # 3. BMI Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["BMI"], bins=20, kde=True)
    plt.title("BMI Distribution")
    plt.savefig("graphs/bmi_distribution.png")
    plt.close()

    # 4. Cardiac Risk Level
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Cardiac_Risk_Level")
    plt.title("Cardiac Risk Level Distribution")
    plt.savefig("graphs/cardiac_risk_distribution.png")
    plt.close()

    # 5. Smoking Status
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Smoking_Status")
    plt.title("Smoking Status")
    plt.savefig("graphs/smoking_status.png")
    plt.close()

    # 6. Cholesterol Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Cholesterol_Level"], bins=20, kde=True)
    plt.title("Cholesterol Level Distribution")
    plt.savefig("graphs/cholesterol_distribution.png")
    plt.close()

    # 7. Blood Sugar Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Blood_Sugar"], bins=20, kde=True)
    plt.title("Blood Sugar Distribution")
    plt.savefig("graphs/blood_sugar_distribution.png")
    plt.close()

    # 8. Chest Pain Type
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x="Chest_Pain_Type")
    plt.title("Chest Pain Type")
    plt.xticks(rotation=45)
    plt.savefig("graphs/chest_pain_type.png")
    plt.close()

    # 9. Clinical Diagnosis
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x="Clinical_Diagnosis")
    plt.title("Clinical Diagnosis")
    plt.xticks(rotation=45)
    plt.savefig("graphs/clinical_diagnosis.png")
    plt.close()

    # 10. Diagnosis vs Risk Level
    plt.figure(figsize=(14, 6))
    sns.countplot(
        data=df,
        x="Clinical_Diagnosis",
        hue="Cardiac_Risk_Level"
    )
    plt.title("Clinical Diagnosis vs Cardiac Risk Level")
    plt.xticks(rotation=45)
    plt.savefig("graphs/diagnosis_vs_risk.png")
    plt.close()

    # 11. Systolic BP Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Systolic_BP"], bins=20, kde=True)
    plt.title("Systolic Blood Pressure")
    plt.savefig("graphs/systolic_bp.png")
    plt.close()

    # 12. Correlation Heatmap
    numeric_cols = [
        "Age",
        "Height_cm",
        "Weight_kg",
        "BMI",
        "Systolic_BP",
        "Diastolic_BP",
        "Resting_Heart_Rate",
        "Max_Heart_Rate_Achieved",
        "Cholesterol_Level",
        "Blood_Sugar"
    ]

    # Convert columns to numeric, coercing errors to NaN
    numeric_df = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="Blues"
    )

    plt.title("Correlation Heatmap")
    plt.savefig("graphs/correlation_heatmap.png")
    plt.close()

    print("All graphs generated successfully!")
    print("Graphs saved in 'graphs' folder.")


# Main Program
if __name__ == "__main__":

    print("Loading Heart Patient Dataset...")

    df = load_data()

    print("Dataset Loaded Successfully!")
    print(df.head())

    print("Generating Graphs...")

    generate_all_graphs(df)