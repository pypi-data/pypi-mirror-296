import jpype 
from asposepdf import Assist 


class operators_BX(Assist.BaseJavaClass):
    """!Class representing BX operator (begin compatibility section)."""

    java_class_name = "com.aspose.python.pdf.operators.BX"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
