import jpype 
from asposepdf import Assist 


class operators_TextShowOperator(Assist.BaseJavaClass):
    """!Abstract base class for all operators which used to out text (Tj, TJ, etc)."""

    java_class_name = "com.aspose.python.pdf.operators.TextShowOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
