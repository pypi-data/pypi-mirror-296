import jpype 
from asposepdf import Assist 


class Matrix3D(Assist.BaseJavaClass):
    """!Class represents transformation matrix."""

    java_class_name = "com.aspose.python.pdf.Matrix3D"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
