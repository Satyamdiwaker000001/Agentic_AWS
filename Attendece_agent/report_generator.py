def generate_safe_report(
    report_df,
    output_path="outputs/safe_employees.csv"
):

    safe_df = report_df[
        report_df["Status"] == "SAFE"
    ]

    safe_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Safe report saved: {output_path}"
    )


def generate_danger_report(
    report_df,
    output_path="outputs/danger_employees.csv"
):

    danger_df = report_df[
        report_df["Status"] == "DANGER"
    ]

    danger_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Danger report saved: {output_path}"
    )