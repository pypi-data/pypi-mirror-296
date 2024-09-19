import jpype 
from asposepdf import Assist 


class Point3D(Assist.BaseJavaClass):
    """!Represent point with fractional coordinates."""

    java_class_name = "com.aspose.python.pdf.Point3D"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
