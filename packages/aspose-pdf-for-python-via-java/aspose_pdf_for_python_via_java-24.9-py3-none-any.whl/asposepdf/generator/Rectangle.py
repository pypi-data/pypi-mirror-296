import jpype
from asposepdf import Assist


class Rectangle(Assist.BaseJavaClass):
    """!
    Class represents rectangle.
    """

    javaClassName = "com.aspose.python.pdf.Rectangle"

    def __init__(self, llx: float, lly: float, urx: float, ury: float, normalizeCoordinates: bool = None):
        """!
        Constructor of Rectangle.
        Parameters:
        - llx (float): The x-coordinate of the lower-left corner.
        - lly (float): The y-coordinate of the lower-left corner.
        - urx (float): The x-coordinate of the upper-right corner.
        - ury (float): The y-coordinate of the upper-right corner.
        - normalizeCoordinates (bool): Normalize coordinates of rectangle.
        """
        javaClass = jpype.JClass(self.javaClassName)
        if normalizeCoordinates is None:
            self.javaClass = javaClass(llx, lly, urx, ury)
        else:
            self.javaClass = javaClass(llx, lly, urx, ury, normalizeCoordinates)

