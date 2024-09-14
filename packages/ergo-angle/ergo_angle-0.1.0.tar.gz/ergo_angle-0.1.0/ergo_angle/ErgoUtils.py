import cv2
import math
import time
import numpy as np

def angle_two_lines(dist1: float, dist2: float) -> float:
    """
    Calculates the angle between two lines using their distances.

    Args:
        dist1 (float): The distance of the first line.
        dist2 (float): The distance of the second line.

    Returns:
        float: The angle between the two lines in degrees.
    """
    angle = math.acos(dist1 / dist2)
    return math.degrees(angle)

def projected_point(point_1: list, point_2: list, y_target: float) -> list:
    """
    Projects a point onto a line defined by two points.

    Args:
        point_1 (list): The coordinates of the first point on the line.
        point_2 (list): The coordinates of the second point on the line.
        y_target (float): The y-coordinate where the projection is made.

    Returns:
        list: The coordinates of the projected point.
    """
    x_1, y_1 = point_1
    x_2, y_2 = point_2
    m = (y_2 - y_1) / (x_2 - x_1)
    x_target = int((y_target - y_1 + m * x_1) / m)
    return [x_target, y_target]

def draw_point(frame: any, coordinate: list, color: str = 'green',
               radius: int = 3, outline: int = -1) -> any:
    """
    Draws a point on the frame.

    Args:
        frame (any): The frame on which the point is drawn.
        coordinate (list): The coordinates of the point.
        color (str): The color of the point (default is 'green').
        radius (int): The radius of the point (default is 3).
        outline (int): The thickness of the point outline (default is -1 for filled).

    Returns:
        any: The frame with the drawn point.
    """
    if color.lower() == "red":
        color = (0, 0, 255)
    elif color.lower() == "green":
        color = (0, 255, 0)
    else:  # blue
        color = (255, 0, 0)
    return cv2.circle(frame, coordinate, radius, color, outline)
    
def draw_line(frame: any, point_1: list, point_2: list,
              color: tuple = (0, 0, 255), thickness: int = 2) -> any:
    """
    Draws a line between two points on the frame.

    Args:
        frame (any): The frame on which the line is drawn.
        point_1 (list): The coordinates of the first point.
        point_2 (list): The coordinates of the second point.
        color (tuple): The color of the line (default is red).
        thickness (int): The thickness of the line (default is 2).

    Returns:
        any: The frame with the drawn line.
    """
    return cv2.line(frame, point_1, point_2, color, thickness)

def draw_rectangle(frame: any, pointTop: list, pointBottom: list) -> any:
    """
    Draws a rectangle on the frame.

    Args:
        frame (any): The frame on which the rectangle is drawn.
        pointTop (list): The coordinates of the top-left corner of the rectangle.
        pointBottom (list): The coordinates of the bottom-right corner of the rectangle.

    Returns:
        any: The frame with the drawn rectangle.
    """
    return cv2.rectangle(frame, pointTop, pointBottom,
                         color=(255, 0, 255), thickness=2)

def addText(frame: any, text, coordinate: list, font=cv2.FONT_HERSHEY_SIMPLEX,
            fontsize: float = 0.5, color: tuple = (255, 0, 255), thickness: int = 2) -> any:
    """
    Adds text to the frame.

    Args:
        frame (any): The frame on which the text is added.
        text: The text to be added.
        coordinate (list): The coordinates where the text is added.
        font: The font type (default is cv2.FONT_HERSHEY_SIMPLEX).
        fontsize (float): The font size (default is 0.5).
        color (tuple): The color of the text (default is magenta).
        thickness (int): The thickness of the text (default is 2).

    Returns:
        any: The frame with the added text.
    """
    if isinstance(text, (np.int64, np.float64)):
        return cv2.putText(frame, str(round(text, 1)), coordinate, font, fontsize, color, thickness)
    else:
        return cv2.putText(frame, text, coordinate, font, fontsize, color, thickness)

def midpoint(point1: list, point2: list) -> list:
    """
    Calculates the midpoint between two points.

    Args:
        point1 (list): The coordinates of the first point.
        point2 (list): The coordinates of the second point.

    Returns:
        list: The coordinates of the midpoint.
    """
    if point1.count(0) > 1:
        return point2
    if point2.count(0) > 1:
        return point1
    
    x_1, y_1 = point1
    x_2, y_2 = point2
    mid_x = (x_1 + x_2) / 2
    mid_y = (y_1 + y_2) / 2
    return [int(mid_x), int(mid_y)]

def extend_point(point1: list, point2: list, target_point: list) -> list:
    """
    Extends a point along the line defined by two points, using a target y-coordinate.

    Args:
        point1 (list): The coordinates of the first point on the line.
        point2 (list): The coordinates of the second point on the line.
        target_point (list): The coordinates of the target point.

    Returns:
        list: The coordinates of the extended point.
    """
    x_1, y_1 = point1
    x_2, y_2 = point2
    y_target = target_point[1]
    m = (y_2 - y_1) / (x_2 - x_1)
    x_target = int((y_target - y_1 + m * x_1) / m)
    return [x_target, y_target]

def normalize_point(base_point: list, target_point: list) -> list:
    """
    Normalizes the coordinates of a target point relative to a base point.

    Args:
        base_point (list): The coordinates of the base point.
        target_point (list): The coordinates of the target point.

    Returns:
        list: The normalized coordinates.
    """
    x_n = target_point[0] - base_point[0] 
    y_n = target_point[1] - base_point[1]
    return [x_n, y_n]

def calculate_angle(base_point: list, point1: list, point2: list) -> float:
    """
    Calculates the angle between two vectors originating from a base point.

    Args:
        base_point (list): The coordinates of the base point.
        point1 (list): The coordinates of the first point.
        point2 (list): The coordinates of the second point.

    Returns:
        float: The angle between the two vectors in degrees.
    """
    point1_n = normalize_point(base_point, point1)
    point2_n = normalize_point(base_point, point2)
    angle1 = abs(math.degrees(math.atan2(point1_n[1], point1_n[0])))
    angle2 = abs(math.degrees(math.atan2(point2_n[1], point2_n[0])))
    result_angle = abs(angle2 - angle1)
    return result_angle

def check_zero_points(*points: list) -> bool:
    """
    Checks if any of the provided points have coordinates (0,0).

    Args:
        *points (list): A variable number of points to check.

    Returns:
        bool: True if none of the points have coordinates (0,0), False otherwise.
    """
    for point in points:
        if point.count(0) > 1:
            return False
    return True

def warning_counts(frame: any, output: str) -> None:
    """
    Displays a warning counter on the frame if the output is "WARNING".

    Args:
        frame (any): The frame on which the warning is displayed.
        output (str): The output string which triggers the warning.
    """
    global start_time, time_counter
    if output == "WARNING":
        if start_time is None:
            start_time = time.time()
        else:
            time_counter += time.time() - start_time
            start_time = time.time()
    else:
        start_time = None
        
    cv2.putText(frame, f"Time Counter: {time_counter:.2f}s", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
