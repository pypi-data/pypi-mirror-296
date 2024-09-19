import jpype 
from asposepdf import Assist 


class operators_SetHorizontalTextScaling(Assist.BaseJavaClass):
    """!Class representing Tz operator (set horizontal text scaling)."""

    java_class_name = "com.aspose.python.pdf.operators.SetHorizontalTextScaling"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
