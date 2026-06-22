import cv2
import time

from hand_tracker import HandTracker
from instrument_controller import InstrumentController


cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

tracker = HandTracker()

piano = InstrumentController()

notes = [
    "C",
    "D",
    "E",
    "F",
    "G",
    "A",
    "B"
]

last_note = ""
last_time = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(
        frame,
        1
    )

    frame = cv2.resize(
        frame,
        (900, 600)
    )

    frame = tracker.find_hands(
        frame
    )

    landmarks = tracker.get_landmarks(
        frame
    )

    h, w, _ = frame.shape

    piano_top = 450
    key_width = w // 7

    active_note = ""

    # Draw Piano
    for i, note in enumerate(notes):

        x1 = i * key_width
        x2 = (i + 1) * key_width

        cv2.rectangle(
            frame,
            (x1, piano_top),
            (x2, h),
            (255, 255, 255),
            -1
        )

        cv2.rectangle(
            frame,
            (x1, piano_top),
            (x2, h),
            (0, 0, 0),
            2
        )

        cv2.putText(
            frame,
            note,
            (x1 + 45, 560),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 0),
            3
        )

    if landmarks:

        index_tip = landmarks[8]

        x = index_tip[1]
        y = index_tip[2]

        cv2.circle(
            frame,
            (x, y),
            12,
            (0, 0, 255),
            cv2.FILLED
        )

        if y > piano_top:

            note_index = min(
                x // key_width,
                6
            )

            active_note = notes[note_index]

            current_time = time.time()

            if (
                active_note != last_note
                or
                current_time - last_time > 0.3
            ):

                piano.play_note(
                    active_note
                )

                last_note = active_note
                last_time = current_time

    cv2.rectangle(
        frame,
        (0, 0),
        (900, 60),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        frame,
        f"Playing: {active_note}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Virtual Piano",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()