import jpype 
from asposepdf import Assist 


class operators_SetCharWidthBoundingBox(Assist.BaseJavaClass):
    """!Class representing d1 operator (set glyph and bounding box)."""

    java_class_name = "com.aspose.python.pdf.operators.SetCharWidthBoundingBox"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
