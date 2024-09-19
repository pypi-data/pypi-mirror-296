import jpype 
from asposepdf import Assist 


class operators_GS(Assist.BaseJavaClass):
    """!Class representing gs operator (set parameters from graphic state parameter dictionary)."""

    java_class_name = "com.aspose.python.pdf.operators.GS"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
