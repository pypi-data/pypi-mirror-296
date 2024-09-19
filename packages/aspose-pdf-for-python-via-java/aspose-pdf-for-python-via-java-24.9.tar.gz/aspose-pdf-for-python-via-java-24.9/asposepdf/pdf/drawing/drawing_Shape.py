import jpype 
from asposepdf import Assist 


class drawing_Shape(Assist.BaseJavaClass):
    """!Represents shape - the base graphics object."""

    java_class_name = "com.aspose.python.pdf.drawing.Shape"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
