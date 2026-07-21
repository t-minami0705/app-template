import inspect

import cv2
import numpy as np

from core.com.BaseResult import BaseResult
from dataclasses import dataclass

# ========================================================================================
# Rectangle Data Class
# ========================================================================================
@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int
    line_color: tuple[int, int, int]
    fill_color: tuple[int, int, int]
    points: list[tuple[int, int]]

    # ========================================================================================
    # Factory Method
    # ========================================================================================
    @classmethod
    def from_xywh(
            cls,
            x: int, y: int,
            width: int, height: int,
            line_color: tuple[int, int, int], fill_color: tuple[int, int, int]
        ) -> 'Rectangle':
        """ Create a rectangle from the given parameters.
        :param x: Point X, the origin of the figure.
        :param y: Point Y, the origin of the figure.
        :param width: Width from the starting point coordinates.
        :param height: Height from the starting point coordinates.
        :param line_color: Frame color to draw.
        :param fill_color: Fill color to draw.
        :return: A Rectangle object.
        """
        points = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]

        return cls(
                x=x,
                y=y,
                width=width,
                height=height,
                line_color=line_color,
                fill_color=fill_color,
                points=points
            )

    @classmethod
    def from_points(
            cls,
            points: list[tuple[int, int]],
            line_color: tuple[int, int, int],
            fill_color: tuple[int, int, int]
        ) -> 'Rectangle':
        """ Create a rectangle from the given points.
        :param points: List of points defining the rectangle.
        :param line_color: Frame color to draw.
        :param fill_color: Fill color to draw.
        :return: A Rectangle object.
        """
        x = min(point[0] for point in points)
        y = min(point[1] for point in points)

        width = max(point[0] for point in points) - x
        height = max(point[1] for point in points) - y

        return cls(
                x=x,
                y=y,
                width=width,
                height=height,
                line_color=line_color,
                fill_color=fill_color,
                points=points
            )
    
    # ========================================================================================
    # Methods
    # ========================================================================================
    # Recalculation Method When Changing Corner Points
    def update_from_points(self) -> None:
        """ Update the rectangle's position and size based on new points.
        :param points: List of points defining the new rectangle.
        """
        self.x = min(point[0] for point in self.points)
        self.y = min(point[1] for point in self.points)
        self.width = max(point[0] for point in self.points) - self.x
        self.height = max(point[1] for point in self.points) - self.y

    # Method to recalculate a point when the X or Y coordinates of its four corners are changed
    def update_points(self) -> None:
        """ Update the rectangle's points based on its position and size. """
        self.points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height)
        ]
    
    # Recalculating Anchor Points When the Width Changes (Left-Side Anchor, Right-Side Adjustment)
    def update_points_from_width(self, new_width: int):
        """ Update the rectangle's points based on a new width.
        :param new_width: The new width of the rectangle.
        """
        old_width = self.width
        if old_width == 0:
            return

        ratio = new_width / old_width

        left_x = min(p[0] for p in self.points)
        right_x = max(p[0] for p in self.points)

        new_right_x = left_x + new_width

        new_points = []

        for x, y in self.points:
            if x == right_x:
                new_points.append((new_right_x, y))
            else:
                new_points.append((x, y))

        self.points = new_points
        self.width = new_width

    # Recalculating Points When the Height Is Changed (Top as Starting Point, Bottom Adjusted)
    def update_points_from_height(self, new_height: int):
        """ Update the rectangle's points based on a new height.
        :param new_height: The new height of the rectangle.
        """
        old_height = self.height
        if old_height == 0:
            return

        top_y = min(p[1] for p in self.points)
        bottom_y = max(p[1] for p in self.points)

        new_bottom_y = top_y + new_height

        new_points = []

        for x, y in self.points:
            if y == bottom_y:
                new_points.append((x, new_bottom_y))
            else:
                new_points.append((x, y))

        self.points = new_points
        self.height = new_height

# ========================================================================================
# Rectangle Data Class
# ========================================================================================
class RectangleManager:
    """ Image processing class
    author: T.Minami
    version: 1.0.0
    since: 1.0.0
    note:
        This is a class that generates a rectangle diagram using OPenCV.
        In addition to basic functionality, it also provides features related to shape processing.
    """
    # ========================================================================================
    # Constructor / Destructor
    # ========================================================================================
    def __init__(self):
        """ Initialize the rectangle information.
        :param x: Point X, the origin of the figure.
        :param y: Point Y, the origin of the figure.
        :param width:Width from the starting point coordinates.
        :param height:Height from the starting point coordinates.
        :param color:Frame color to drow.
        """
        super().__init__()
        self._rectangles: list[Rectangle] = []

    # ========================================================================================
    # Properties
    # ========================================================================================


    # ========================================================================================
    # Collection operations
    # ========================================================================================
    def add_rectangle(self, rectangle: Rectangle) -> None:
        """ Add a rectangle to the list.
        :param rectangle: Rectangle object to add.
        """
        self._rectangles.append(rectangle)
    
    def get_rectangles(self) -> list[Rectangle]:
        """ Get the list of rectangles.
        :return: List of Rectangle objects.
        """
        return self._rectangles
    
    def remove_rectangle(self, rectangle: Rectangle) -> None:
        """ Remove a rectangle from the list.
        :param rectangle: Rectangle object to remove.
        """
        self._rectangles.remove(rectangle)
    
    def clear_rectangles(self) -> None:
        """ Clear all rectangles from the list. """
        self._rectangles.clear()    

    def count_rectangles(self) -> int:
        """ Get the count of rectangles in the list.
        :return: Count of Rectangle objects.
        """
        return len(self._rectangles)
    
