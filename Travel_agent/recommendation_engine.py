# ============================================================
# IMPORTS
# ============================================================

import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


# ============================================================
# FEATURE 10 : BUDGET RECOMMENDATION
# ============================================================

def recommend_by_budget(df, budget):

    temp_df = df.copy()

    temp_df["Accommodation cost"] = pd.to_numeric(
        temp_df["Accommodation cost"],
        errors="coerce"
    ).fillna(0)

    temp_df["Transportation cost"] = pd.to_numeric(
        temp_df["Transportation cost"],
        errors="coerce"
    ).fillna(0)

    temp_df["Total Cost"] = (
        temp_df["Accommodation cost"]
        +
        temp_df["Transportation cost"]
    )

    filtered = temp_df[
        temp_df["Total Cost"] <= budget
    ]

    if filtered.empty:
        return pd.Series(name="Total Cost", dtype=float)

    recommendations = (
        filtered.groupby("Destination")
        ["Total Cost"]
        .mean()
        .sort_values()
        .head(5)
    )

    return recommendations


# ============================================================
# FEATURE 11 : CHEAPEST DESTINATION FINDER
# ============================================================

def cheapest_destinations(df):

    temp_df = df.copy()

    temp_df["Accommodation cost"] = pd.to_numeric(
        temp_df["Accommodation cost"],
        errors="coerce"
    ).fillna(0)

    temp_df["Transportation cost"] = pd.to_numeric(
        temp_df["Transportation cost"],
        errors="coerce"
    ).fillna(0)

    temp_df["Total Cost"] = (
        temp_df["Accommodation cost"]
        +
        temp_df["Transportation cost"]
    )

    if temp_df.empty:
        return pd.Series(name="Total Cost", dtype=float)

    cheapest = (
        temp_df.groupby("Destination")
        ["Total Cost"]
        .mean()
        .sort_values()
        .head(10)
    )

    return cheapest


# ============================================================
# INTERNAL FUNCTION : CLEAN COST COLUMNS
# ============================================================

def clean_cost_columns(df):

    temp_df = df.copy()

    cost_columns = [
        "Accommodation cost",
        "Transportation cost"
    ]

    for column in cost_columns:

        temp_df[column] = (
            temp_df[column]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        temp_df[column] = pd.to_numeric(
            temp_df[column],
            errors="coerce"
        )

        temp_df[column] = (
            temp_df[column]
            .fillna(0)
        )

    return temp_df


# ============================================================
# FEATURE 12 : COST PREDICTION MODEL TRAINING
# ============================================================

def train_cost_model(df):

    model_df = clean_cost_columns(df)

    # --------------------------------------------------------
    # CREATE TOTAL COST
    # --------------------------------------------------------

    model_df["Total Cost"] = (
        model_df["Accommodation cost"]
        +
        model_df["Transportation cost"]
    )

    # --------------------------------------------------------
    # ENCODE DESTINATION
    # --------------------------------------------------------

    destination_encoder = LabelEncoder()

    model_df["Destination_Encoded"] = (
        destination_encoder.fit_transform(
            model_df["Destination"]
        )
    )

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    X = model_df[
        [
            "Duration (days)",
            "Destination_Encoded"
        ]
    ]

    y = model_df["Total Cost"]

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    print("[SUCCESS] Cost Model Trained")

    return model, destination_encoder


# ============================================================
# FEATURE 12 : COST PREDICTION
# ============================================================

def predict_trip_cost(
    model,
    encoder,
    destination,
    duration
):

    try:

        encoded_destination = encoder.transform(
            [destination]
        )[0]

        prediction = model.predict(
            [[
                duration,
                encoded_destination
            ]]
        )

        return round(
            float(prediction[0]),
            2
        )

    except Exception as e:

        print(
            f"[ERROR] Prediction Failed: {e}"
        )

        return 0


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    print(
        "Recommendation Engine Loaded Successfully"
    )