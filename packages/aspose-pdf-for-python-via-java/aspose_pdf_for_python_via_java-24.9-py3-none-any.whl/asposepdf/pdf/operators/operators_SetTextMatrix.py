import jpype 
from asposepdf import Assist 


class operators_SetTextMatrix(Assist.BaseJavaClass):
    """!Class representig Tm operator (set text matrix)."""

    java_class_name = "com.aspose.python.pdf.operators.SetTextMatrix"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
