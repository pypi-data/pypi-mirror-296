import jpype 
from asposepdf import Assist 


class operators_TextStateOperator(Assist.BaseJavaClass):
    """!Abstract base class for operators which changes current text state (Tc, Tf, TL, etc)."""

    java_class_name = "com.aspose.python.pdf.operators.TextStateOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
