import jpype 
from asposepdf import Assist 


class operators_SetColorOperator(Assist.BaseJavaClass):
    """!Class representing set color operation."""

    java_class_name = "com.aspose.python.pdf.operators.SetColorOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
