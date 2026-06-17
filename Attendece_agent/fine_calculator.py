def calculate_fine(minutes_late):

    if minutes_late <= 15:
        return 50

    elif minutes_late <= 30:
        return 100

    elif minutes_late <= 60:
        return 200

    return 500