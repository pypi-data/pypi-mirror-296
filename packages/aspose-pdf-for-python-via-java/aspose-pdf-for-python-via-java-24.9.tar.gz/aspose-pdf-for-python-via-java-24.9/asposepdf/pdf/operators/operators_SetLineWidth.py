import jpype 
from asposepdf import Assist 


class operators_SetLineWidth(Assist.BaseJavaClass):
    """!Class representing w operator (set line width)."""

    java_class_name = "com.aspose.python.pdf.operators.SetLineWidth"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
