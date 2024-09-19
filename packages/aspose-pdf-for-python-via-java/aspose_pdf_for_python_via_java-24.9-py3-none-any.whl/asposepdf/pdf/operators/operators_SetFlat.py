import jpype 
from asposepdf import Assist 


class operators_SetFlat(Assist.BaseJavaClass):
    """!Class representing i operator (set flatness toleracne)."""

    java_class_name = "com.aspose.python.pdf.operators.SetFlat"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
