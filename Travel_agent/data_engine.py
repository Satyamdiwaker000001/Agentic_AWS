# ============================================================
# IMPORTS
# ============================================================

import pandas as pd
from typing import Optional


# ============================================================
# FEATURE 01 : DATASET LOADING
# ============================================================

def load_dataset(
    file_path: str
) -> Optional[pd.DataFrame]:
    """
    Load travel dataset from CSV file.
    """

    try:

        df = pd.read_csv(file_path)

        print(f"[SUCCESS] Dataset Loaded")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except Exception as e:

        print(f"[ERROR] Unable to load dataset")
        print(e)

        return None
# ============================================================
# FEATURE 02 : DATASET VALIDATION
# ============================================================

def validate_dataset(df: pd.DataFrame) -> bool:
    """
    Validate required columns.
    """

    required_columns = [
        "Destination",
        "Duration (days)",
        "Traveler gender",
        "Traveler nationality",
        "Accommodation type",
        "Accommodation cost",
        "Transportation type",
        "Transportation cost"
    ]

    missing_columns = []

    for column in required_columns:

        if column not in df.columns:
            missing_columns.append(column)

    if len(missing_columns) > 0:

        print("\n[VALIDATION FAILED]")
        print("Missing Columns:")

        for col in missing_columns:
            print(f"- {col}")

        return False

    print("\n[SUCCESS] Dataset Validation Passed")

    return True


# ============================================================
# FEATURE 03 : DATASET CLEANING
# ============================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset and remove bad records.
    """

    original_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing text values
    text_columns = [
        "Destination",
        "Traveler gender",
        "Traveler nationality",
        "Accommodation type",
        "Transportation type"
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    # Fill missing numeric values
    numeric_columns = [
        "Duration (days)",
        "Accommodation cost",
        "Transportation cost"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = df[column].fillna(0)

    cleaned_rows = len(df)

    print("\n[CLEANING COMPLETE]")
    print(f"Original Rows : {original_rows}")
    print(f"Final Rows    : {cleaned_rows}")

    return df


# ============================================================
# COST COLUMN CLEANING
# ============================================================

cost_columns = [
    "Accommodation cost",
    "Transportation cost"
]

for column in cost_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        df[column] = df[column].fillna(0)

# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    FILE_PATH = "Travel details dataset.csv"

    df = load_dataset(FILE_PATH)

    if df is not None:

        if validate_dataset(df):

            df = clean_dataset(df)

            print("\nDataset Ready For RAG Pipeline")