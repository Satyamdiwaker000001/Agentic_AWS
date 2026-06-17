from datetime import datetime

from Agentic.Attendece_agent.fine_calculator import calculate_fine


def analyze_attendance(attendance_value):

    try:

        check_in = attendance_value.split("-")[0]

        office_time = datetime.strptime(
            "09:00",
            "%H:%M"
        )

        employee_time = datetime.strptime(
            check_in,
            "%H:%M"
        )

        if employee_time <= office_time:

            return "SAFE", 0, 0

        minutes_late = int(
            (
                employee_time - office_time
            ).total_seconds() / 60
        )

        fine = calculate_fine(
            minutes_late
        )

        return (
            "DANGER",
            minutes_late,
            fine
        )

    except:

        return (
            "INVALID",
            0,
            0
        )
    
