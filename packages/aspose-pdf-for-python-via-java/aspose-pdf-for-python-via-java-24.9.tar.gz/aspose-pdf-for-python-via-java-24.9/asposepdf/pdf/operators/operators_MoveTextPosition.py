import jpype 
from asposepdf import Assist 


class operators_MoveTextPosition(Assist.BaseJavaClass):
    """!Class representing Td operator (move text position)."""

    java_class_name = "com.aspose.python.pdf.operators.MoveTextPosition"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
