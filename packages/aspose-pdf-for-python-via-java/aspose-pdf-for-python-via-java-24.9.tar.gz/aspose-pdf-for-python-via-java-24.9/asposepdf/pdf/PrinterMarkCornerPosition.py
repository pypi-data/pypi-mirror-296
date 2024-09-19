import jpype 
from asposepdf import Assist 


class PrinterMarkCornerPosition(Assist.BaseJavaClass):
    """!Represents a position of a mark in a corner of a page."""

    java_class_name = "com.aspose.python.pdf.PrinterMarkCornerPosition"
    java_class = jpype.JClass(java_class_name)

    TopLeft = java_class.TopLeft
    """!
     Position the mark in the top left corner.
    
    """

    TopRight = java_class.TopRight
    """!
     Position the mark in the top right corner.
    
    """

    BottomLeft = java_class.BottomLeft
    """!
     Position the mark in the bottom left corner.
    
    """

    BottomRight = java_class.BottomRight
    """!
     Position the mark in the bottom right corner.
    
    """

