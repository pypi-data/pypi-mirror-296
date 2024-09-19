import jpype 
from asposepdf import Assist 


class operators_SetCMYKColor(Assist.BaseJavaClass):
    """!Class representing k operator (set CMYK color for non-stroking operations)."""

    java_class_name = "com.aspose.python.pdf.operators.SetCMYKColor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
