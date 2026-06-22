from utils import distance


class GestureDetector:

    def detect(self, landmarks):

        if not landmarks:
            return "NONE"

        index_tip = landmarks[8]
        middle_tip = landmarks[12]

        dist = distance(
            index_tip[1],
            index_tip[2],
            middle_tip[1],
            middle_tip[2]
        )

        if dist < 40:
            return "CLICK"

        return "MOVE"