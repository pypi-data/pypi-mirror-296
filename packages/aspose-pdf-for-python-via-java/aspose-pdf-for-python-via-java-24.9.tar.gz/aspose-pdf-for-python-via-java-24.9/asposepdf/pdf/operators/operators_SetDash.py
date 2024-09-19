import jpype 
from asposepdf import Assist 


class operators_SetDash(Assist.BaseJavaClass):
    """!Class representing d operator (set line dash pattern)."""

    java_class_name = "com.aspose.python.pdf.operators.SetDash"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
