import jpype 
from asposepdf import Assist 


class operators_SetTextRise(Assist.BaseJavaClass):
    """!Class representing Ts operator (set text rise)."""

    java_class_name = "com.aspose.python.pdf.operators.SetTextRise"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
