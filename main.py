"""
Student Data Explorer

What this project does (simple workflow):
1) Load a CSV dataset
2) Clean the data (convert types, handle missing values)
3) Create a useful feature (average_score)
4) Summarise insights (averages, top/lowest student, correlations)
5) Export outputs (cleaned CSV + summary text report)

Why this structure?
- Splitting into functions makes it easier to read, debug, test, and explain.
"""

import pandas as pd

DATA_FILE = "students.csv"


-
# 1) Load data

def load_data(path: str) -> pd.DataFrame:
    """
    Reads the CSV file into a pandas DataFrame.

    A DataFrame is like a spreadsheet in Python:
    rows = records, columns = fields.
    """
    df = pd.read_csv(path)
    return df



# 2) Validate expected columns

def ensure_columns_exist(df: pd.DataFrame, required_cols: list[str]) -> None:
    """
    Checks the dataset has the columns we expect.
    If something is missing, we raise an error with a clear message.
    """
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Found columns: {list(df.columns)}")



# 3) Clean data + track what we fixed

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Cleans the dataset so analysis is reliable.

    What we do:
    - Convert key columns to numeric (invalid values become NaN)
    - Fill missing physics values with the physics column mean
      (simple and easy to explain)

    Returns:
    - cleaned DataFrame
    - a small quality report (e.g. how many missing values we fixed)
    """
    numeric_cols = ["maths", "computer_science", "physics", "study_hours", "attendance"]
    ensure_columns_exist(df, ["student_id"] + numeric_cols)

    # Count missing values BEFORE cleaning
    before_missing = df[numeric_cols].isna().sum().to_dict()

    # Convert columns to numeric safely
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # invalid strings -> NaN

    # Fill missing physics values with the mean (only if needed)
    physics_missing_before_fill = int(df["physics"].isna().sum())
    if physics_missing_before_fill > 0:
        df["physics"] = df["physics"].fillna(df["physics"].mean())

    # Count missing values AFTER cleaning
    after_missing = df[numeric_cols].isna().sum().to_dict()

    quality_report = {
        "missing_before": before_missing,
        "missing_after": after_missing,
        "physics_missing_filled": physics_missing_before_fill,
    }

    return df, quality_report



# 4) Add features (extra useful columns)

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a new column 'average_score' so we can compare performance easily.
    """
    df["average_score"] = df[["maths", "computer_science", "physics"]].mean(axis=1)
    return df



# 5) Summarise insights

def summarise(df: pd.DataFrame) -> dict:
    """
    Produces summary statistics and simple insights.

    Correlation notes:
    - +1 means strong positive relationship (both rise together)
    -  0 means little/no relationship
    - -1 means strong negative relationship (one rises, other falls)
    """
    summary = {
        "rows": len(df),
        "average_maths": round(df["maths"].mean(), 2),
        "average_cs": round(df["computer_science"].mean(), 2),
        "average_physics": round(df["physics"].mean(), 2),
        "average_study_hours": round(df["study_hours"].mean(), 2),
        "average_attendance": round(df["attendance"].mean(), 2),
        "top_student_by_average": df.loc[df["average_score"].idxmax(), "student_id"],
        "top_average_score": round(df["average_score"].max(), 2),
        "lowest_student_by_average": df.loc[df["average_score"].idxmin(), "student_id"],
        "lowest_average_score": round(df["average_score"].min(), 2),
        "corr_study_vs_average": round(df["study_hours"].corr(df["average_score"]), 3),
        "corr_attendance_vs_average": round(df["attendance"].corr(df["average_score"]), 3),
    }
    return summary



# 6) Save outputs

def save_outputs(df: pd.DataFrame, summary: dict, quality_report: dict) -> None:
    """
    Exports the cleaned dataset and a readable summary report.
    """
    df.to_csv("students_cleaned.csv", index=False)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write("Student Data Explorer — Summary Report\n")
        f.write("-------------------------------------\n\n")

        f.write("Data Quality\n")
        f.write("-----------\n")
        f.write(f"Physics missing values filled: {quality_report['physics_missing_filled']}\n")
        f.write(f"Missing before cleaning: {quality_report['missing_before']}\n")
        f.write(f"Missing after cleaning:  {quality_report['missing_after']}\n\n")

        f.write("Insights\n")
        f.write("--------\n")
        for k, v in summary.items():
            f.write(f"{k}: {v}\n")


# 
# Main program (runs the pipeline)

def main():
    print("Student Data Explorer")
    print("--------------------")

    # Step 1: Load
    df = load_data(DATA_FILE)
    print(f"Loaded {len(df)} rows from {DATA_FILE}")

    # Step 2: Clean + report quality
    df, quality_report = clean_data(df)
    print("Cleaned data.")
    print(f"- Physics missing filled: {quality_report['physics_missing_filled']}")

    # Step 3: Feature engineering
    df = add_features(df)
    print("Added feature: average_score")

    # Step 4: Summaries
    summary = summarise(df)

    print("\nKey Insights:")
    print(f"- Average Maths: {summary['average_maths']}")
    print(f"- Average CS: {summary['average_cs']}")
    print(f"- Average Physics: {summary['average_physics']}")
    print(f"- Top student (avg): {summary['top_student_by_average']} ({summary['top_average_score']})")
    print(f"- Study hours vs average score correlation: {summary['corr_study_vs_average']}")
    print(f"- Attendance vs average score correlation: {summary['corr_attendance_vs_average']}")

    # Step 5: Save outputs
    save_outputs(df, summary, quality_report)
    print("\nSaved outputs: students_cleaned.csv and summary.txt")


if __name__ == "__main__":
    main()
