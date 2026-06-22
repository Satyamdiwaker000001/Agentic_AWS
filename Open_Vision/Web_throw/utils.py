import math

def calculate_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def map_coordinates(x, y, src_w, src_h, dest_w, dest_h):
    mapped_x = int((x / src_w) * dest_w)
    mapped_y = int((y / src_h) * dest_h)
    return mapped_x, mapped_y
