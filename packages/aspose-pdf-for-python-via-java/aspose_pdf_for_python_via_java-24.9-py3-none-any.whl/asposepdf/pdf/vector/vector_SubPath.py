import jpype 
from asposepdf import Assist 


class vector_SubPath(Assist.BaseJavaClass):
    """!Represents vector graphics object on the page.
     Basically, vector graphics objects are represented by two groups of SubPaths.
     One of them is represented by a set of lines and curves.
     Others are presented as rectangles and can sometimes be confused.
     Usually it is a rectangular area that has a color, but very often this rectangle
     is placed at the beginning of the page and defines the entire space of the page in white.
     So you get the SubPath, but visually you only see the text on the page."""

    java_class_name = "com.aspose.python.pdf.vector.SubPath"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
