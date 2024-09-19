import jpype 
from asposepdf import Assist 


class operators_CurveTo(Assist.BaseJavaClass):
    """!Class representing c operator (append curve to path)."""

    java_class_name = "com.aspose.python.pdf.operators.CurveTo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
