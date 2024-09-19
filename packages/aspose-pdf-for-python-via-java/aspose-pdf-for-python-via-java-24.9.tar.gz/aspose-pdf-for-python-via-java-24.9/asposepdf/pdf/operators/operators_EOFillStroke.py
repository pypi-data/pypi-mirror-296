import jpype 
from asposepdf import Assist 


class operators_EOFillStroke(Assist.BaseJavaClass):
    """!Class representing B* operator (fill and stroke path usign even-odd rule)."""

    java_class_name = "com.aspose.python.pdf.operators.EOFillStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
