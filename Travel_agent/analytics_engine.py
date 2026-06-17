# ============================================================
# IMPORTS
# ============================================================

import pandas as pd


# ============================================================
# FEATURE 13 : MALE / FEMALE ANALYSIS
# ============================================================

def gender_analysis(df):

    male_df = df[
        df["Traveler gender"]
        == "Male"
    ]

    female_df = df[
        df["Traveler gender"]
        == "Female"
    ]

    result = {
        "male_count": len(male_df),
        "female_count": len(female_df),

        "male_top_destinations":
            male_df["Destination"]
            .value_counts()
            .head(5)
            .to_dict(),

        "female_top_destinations":
            female_df["Destination"]
            .value_counts()
            .head(5)
            .to_dict()
    }

    return result


# ============================================================
# FEATURE 14 : NATIONALITY ANALYSIS
# ============================================================

def nationality_analysis(df):

    return (
        df["Traveler nationality"]
        .value_counts()
        .head(10)
        .to_dict()
    )


# ============================================================
# FEATURE 15 : DASHBOARD STATISTICS
# ============================================================

def dashboard_statistics(df):

    temp_df = df.copy()

    # ========================================================
    # CLEAN COST COLUMNS
    # ========================================================

    temp_df["Accommodation cost"] = (
        pd.to_numeric(
            temp_df["Accommodation cost"],
            errors="coerce"
        )
        .fillna(0)
    )

    temp_df["Transportation cost"] = (
        pd.to_numeric(
            temp_df["Transportation cost"],
            errors="coerce"
        )
        .fillna(0)
    )

    # ========================================================
    # CALCULATE STATS
    # ========================================================

    total_records = len(temp_df)

    total_destinations = (
        temp_df["Destination"]
        .nunique()
    )

    avg_duration = round(
        temp_df["Duration (days)"].mean(),
        2
    )

    avg_accommodation_cost = round(
        temp_df["Accommodation cost"].mean(),
        2
    )

    avg_transport_cost = round(
        temp_df["Transportation cost"].mean(),
        2
    )

    return {

        "total_records":
            total_records,

        "total_destinations":
            total_destinations,

        "average_duration":
            avg_duration,

        "average_accommodation_cost":
            avg_accommodation_cost,

        "average_transportation_cost":
            avg_transport_cost
    }