import jpype 
from asposepdf import Assist 


class drawing_GradientRadialShading(Assist.BaseJavaClass):
    """!Represents gradient radial shading type."""

    java_class_name = "com.aspose.python.pdf.drawing.GradientRadialShading"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
