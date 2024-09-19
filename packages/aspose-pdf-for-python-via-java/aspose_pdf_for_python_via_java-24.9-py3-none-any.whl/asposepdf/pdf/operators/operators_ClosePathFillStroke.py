import jpype 
from asposepdf import Assist 


class operators_ClosePathFillStroke(Assist.BaseJavaClass):
    """!Class representing b operator (close, fill and stroke path with nonzer winding rule)."""

    java_class_name = "com.aspose.python.pdf.operators.ClosePathFillStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
