import jpype 
from asposepdf import Assist 


class Color(Assist.BaseJavaClass):
    """!Represents class for color value which can be expressed in different color space."""

    java_class_name = "com.aspose.python.pdf.Color"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

