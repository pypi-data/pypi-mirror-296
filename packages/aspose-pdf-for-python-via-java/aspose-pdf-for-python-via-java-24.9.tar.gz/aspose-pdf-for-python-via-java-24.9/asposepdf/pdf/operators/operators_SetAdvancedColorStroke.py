import jpype 
from asposepdf import Assist 


class operators_SetAdvancedColorStroke(Assist.BaseJavaClass):
    """!Class representing SCN operator (set color for stroking operations)."""

    java_class_name = "com.aspose.python.pdf.operators.SetAdvancedColorStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
