
import os
import pandas as pd

from Agentic.Attendece_agent.analyzer import analyze_attendance

from Agentic.Attendece_agent.report_generator import (
    generate_safe_report,
    generate_danger_report
)

DATASET_PATH = "data/attendance_2023_2024.csv"


def main():

    print("Loading dataset...")

    df = pd.read_csv(DATASET_PATH)

    print(f"Dataset Shape: {df.shape}")

    employees = [
        col
        for col in df.columns
        if col.startswith("Person_")
    ]

    print(
        f"Employees Found: {len(employees)}"
    )

    results = []

    for _, row in df.iterrows():

        current_date = row["Date"]

        for emp in employees:

            attendance = row[emp]

            status, late_minutes, fine = (
                analyze_attendance(attendance)
            )

            results.append(
                {
                    "Date": current_date,
                    "Employee": emp,
                    "Attendance": attendance,
                    "Status": status,
                    "Late_Minutes": late_minutes,
                    "Fine": fine
                }
            )

    report = pd.DataFrame(results)

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    generate_safe_report(
        report,
        "outputs/safe_employees.csv"
    )

    generate_danger_report(
        report,
        "outputs/danger_employees.csv"
    )

    safe_count = (
        report["Status"] == "SAFE"
    ).sum()

    danger_count = (
        report["Status"] == "DANGER"
    ).sum()

    total_fine = report["Fine"].sum()

    print("\n===== SUMMARY =====")

    print(f"SAFE Employees Records: {safe_count}")
    print(f"DANGER Employees Records: {danger_count}")
    print(f"Total Fine Generated: ₹{total_fine}")

    print("===================")

    print("\nAgent Execution Completed")


if __name__ == "__main__":
    main()
