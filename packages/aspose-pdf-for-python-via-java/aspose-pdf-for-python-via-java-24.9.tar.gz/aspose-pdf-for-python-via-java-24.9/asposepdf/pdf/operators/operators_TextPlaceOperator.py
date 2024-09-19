import jpype 
from asposepdf import Assist 


class operators_TextPlaceOperator(Assist.BaseJavaClass):
    """!Abstract base class for operators which changes text position (Tm, Td, etc)."""

    java_class_name = "com.aspose.python.pdf.operators.TextPlaceOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
