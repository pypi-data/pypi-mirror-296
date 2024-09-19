import jpype 
from asposepdf import Assist 


class operators_MoveTo(Assist.BaseJavaClass):
    """!Class representing {@code operators.m} (move to and begin new subpath)."""

    java_class_name = "com.aspose.python.pdf.operators.MoveTo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
