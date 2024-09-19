import jpype 
from asposepdf import Assist 


class operators_ClosePath(Assist.BaseJavaClass):
    """!Class representing h operator (close path)."""

    java_class_name = "com.aspose.python.pdf.operators.ClosePath"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
