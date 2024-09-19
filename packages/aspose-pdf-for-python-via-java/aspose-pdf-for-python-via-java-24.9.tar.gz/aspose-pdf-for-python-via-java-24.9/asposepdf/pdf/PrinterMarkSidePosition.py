import jpype 
from asposepdf import Assist 


class PrinterMarkSidePosition(Assist.BaseJavaClass):
    """!Represents a position of a registration mark on a page."""

    java_class_name = "com.aspose.python.pdf.PrinterMarkSidePosition"
    java_class = jpype.JClass(java_class_name)

    Top = java_class.Top
    """!
     Position the mark in the top margin of the page.
    
    """

    Bottom = java_class.Bottom
    """!
     Position the mark in the bottom margin of the page.
    
    """

    Left = java_class.Left
    """!
     Position the mark in the left margin of the page.
    
    """

    Right = java_class.Right
    """!
     Position the mark in the right margin of the page.
    
    """

