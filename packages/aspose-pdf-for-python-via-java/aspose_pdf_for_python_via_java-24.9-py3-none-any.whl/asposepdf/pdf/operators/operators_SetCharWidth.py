import jpype 
from asposepdf import Assist 


class operators_SetCharWidth(Assist.BaseJavaClass):
    """!Class representing d0 operator (set glyph width)."""

    java_class_name = "com.aspose.python.pdf.operators.SetCharWidth"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
