import jpype 
from asposepdf import Assist 


class operators_SetRGBColor(Assist.BaseJavaClass):
    """!Class representing rg operator (set RGB color for non-stroking operators)."""

    java_class_name = "com.aspose.python.pdf.operators.SetRGBColor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
