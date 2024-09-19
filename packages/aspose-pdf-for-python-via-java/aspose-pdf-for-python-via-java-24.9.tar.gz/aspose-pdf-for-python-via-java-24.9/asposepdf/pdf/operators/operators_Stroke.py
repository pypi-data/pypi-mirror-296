import jpype 
from asposepdf import Assist 


class operators_Stroke(Assist.BaseJavaClass):
    """!Class representing S operator (stroke path)."""

    java_class_name = "com.aspose.python.pdf.operators.Stroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
