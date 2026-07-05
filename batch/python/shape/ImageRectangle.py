import inspect

import cv2
import numpy as np

from core.com.CommonResponse import CommonResponse

class ImageRectangle(CommonResponse):
    """ Image processing class
    author: T.Minami
    version: 1.0.0
    since: 1.0.0
    note:
        This is a class that generates a rectangle diagram using OPenCV.
        In addition to basic functionality, it also provides features related to shape processing.
    """
    def __init__(self, x: int, y: int, width: int, height:int, color: tuple=(0, 255, 0)):
        """ Initialize the rectangle information.
        :param x: Point X, the origin of the figure.
        :param y: Point Y, the origin of the figure.
        :param width:Width from the starting point coordinates.
        :param height:Height from the starting point coordinates.
        :param color:Frame color to drow.
        """
        super().__init__()
        self.className = self.__class__.__name__

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, canvas: np.ndarray) -> None:
        """ Draw a rectangle on the canvas.
        :param canvas: Image data to draw on.
        """
        self.methodName = inspect.currentframe().f_code.co_name
        
        try:
            cv2.rectangle(
                canvas,
                (self.x, self.y),
                (self.x + self.width, self.y + self.height),
                self.color,
                thickness = 1
            )
            self.resultCode = 0
            self.resultMsg = "Rectangle drawn successfully."
            self.resultErrMsg = ""

        except Exception as e:
            self.resultCode = 801
            self.resultMsg = "Error occurred while drawing rectangle."
            self.resultErrMsg = str(e)

    def overlapsCheck(self, other: 'ImageRectangle') -> bool:
        """ Check if two rectangles overlap.
        :param other: Another ImageRectangle instance.
        :return: True if the rectangles overlap, False otherwise.
        """
        self.methodName = inspect.currentframe().f_code.co_name

        try:
            result = not (
                self.x + self.width <= other.x or
                other.x + other.width <= self.x or
                self.y + self.height <= other.y or
                other.y + other.height <= self.y
            )
            self.resultCode = 0
            self.resultMsg = "Overlap check completed successfully."
            self.resultErrMsg = ""
            return result

        except Exception as e:
            self.resultCode = 802
            self.resultMsg = "Error occurred while checking overlap."
            self.resultErrMsg = str(e)
            return False

    def loadImage(self, canvas: np.ndarray, file_path: str) -> np.ndarray:
        """ Load an image from a file.
        :param canvas: Image data to draw on.
        :param file_path: Path to the image file.
        :return: Loaded image data.
        :raises: FileNotFoundError If the image file does not exist.
        """
        self.methodName = inspect.currentframe().f_code.co_name

        try:
            img = cv2.imread(file_path)
            if img is None:
                raise FileNotFoundError(f"Image file not found: {file_path}")
            h, w = canvas.shape[:2]
            result = cv2.resize(img, (w,h))
            self.resultCode = 0
            self.resultMsg = "Image loaded successfully."
            self.resultErrMsg = ""
            return result
        
        except Exception as e:
            self.resultCode = 803
            self.resultMsg = "Error occurred while loading image."
            self.resultErrMsg = str(e)
            return None


""" Test code for CvRectangle class """
if __name__ == "__main__":
    """ Rectangular Markings on Campus """
    canvas = 255 * np.ones((400, 400, 3), dtype = np.uint8)
    rect1 = ImageRectangle(50, 50, 100, 100, color=(0, 255, 0))
    rect2 = ImageRectangle(60, 60, 50, 50, color=(0, 0, 255))

    rect1.draw(canvas)
    rect2.draw(canvas)

    """ Check for overlap between the two figures """
    if rect1.overlapsCheck(rect2):
        print("They're overlapping.")
    else:
        print("They are not overlapping.")

    cv2.imshow("Canvas", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
