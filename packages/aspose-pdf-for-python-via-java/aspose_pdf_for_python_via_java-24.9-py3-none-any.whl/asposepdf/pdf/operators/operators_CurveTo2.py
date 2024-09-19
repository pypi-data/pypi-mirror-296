import jpype 
from asposepdf import Assist 


class operators_CurveTo2(Assist.BaseJavaClass):
    """!Class representing y operator (append curve to path, final point replicated)."""

    java_class_name = "com.aspose.python.pdf.operators.CurveTo2"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
