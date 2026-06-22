import pyautogui


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = (
            pyautogui.size()
        )

    def move_cursor(self, x, y):

        pyautogui.moveTo(
            x,
            y
        )

    def left_click(self):

        pyautogui.click()