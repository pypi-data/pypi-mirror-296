import jpype 
from asposepdf import Assist 


class operators_SetColor(Assist.BaseJavaClass):
    """!Represents class for sc operator (set color for non-stroking operations)."""

    java_class_name = "com.aspose.python.pdf.operators.SetColor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
