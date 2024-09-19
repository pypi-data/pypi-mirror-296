import jpype 
from asposepdf import Assist 


class operators_SetRGBColorStroke(Assist.BaseJavaClass):
    """!Class representing RG operator (set RGB color for stroking operators)."""

    java_class_name = "com.aspose.python.pdf.operators.SetRGBColorStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
