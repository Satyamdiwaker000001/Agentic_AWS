from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import math

class WebRenderer:
    def __init__(self):
        self.webs = []

    def add_web(self, origin_x, origin_y):
        self.webs.append({
            "x": origin_x,
            "y": origin_y,
            "radius": 10,
            "max_radius": 1200,
            "speed": 60,
            "alpha": 255
        })

    def update(self):
        active_webs = []
        for web in self.webs:
            web["radius"] += web["speed"]
            if web["radius"] > web["max_radius"] / 2:
                web["alpha"] = max(0, web["alpha"] - 15)
            if web["alpha"] > 0:
                active_webs.append(web)
        self.webs = active_webs

    def draw(self, painter: QPainter):
        for web in self.webs:
            pen = QPen(QColor(255, 255, 255, web["alpha"]))
            pen.setWidth(3)
            painter.setPen(pen)
            
            num_lines = 12
            for i in range(num_lines):
                angle = i * (360 / num_lines)
                rad = math.radians(angle)
                end_x = web["x"] + web["radius"] * math.cos(rad)
                end_y = web["y"] + web["radius"] * math.sin(rad)
                painter.drawLine(int(web["x"]), int(web["y"]), int(end_x), int(end_y))
            
            num_circles = 5
            for c in range(1, num_circles + 1):
                r = (web["radius"] / num_circles) * c
                painter.drawEllipse(int(web["x"] - r), int(web["y"] - r), int(r * 2), int(r * 2))
