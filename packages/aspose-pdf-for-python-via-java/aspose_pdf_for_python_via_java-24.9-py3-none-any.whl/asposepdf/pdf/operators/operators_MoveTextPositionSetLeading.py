import jpype 
from asposepdf import Assist 


class operators_MoveTextPositionSetLeading(Assist.BaseJavaClass):
    """!Class representing TD operator (move position and set leading)."""

    java_class_name = "com.aspose.python.pdf.operators.MoveTextPositionSetLeading"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
