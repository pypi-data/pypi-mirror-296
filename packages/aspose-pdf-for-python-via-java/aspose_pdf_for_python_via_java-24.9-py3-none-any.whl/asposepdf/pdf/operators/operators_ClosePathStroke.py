import jpype 
from asposepdf import Assist 


class operators_ClosePathStroke(Assist.BaseJavaClass):
    """!Class representing s operator (Close and stroke path)."""

    java_class_name = "com.aspose.python.pdf.operators.ClosePathStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
