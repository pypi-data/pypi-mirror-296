import jpype 
from asposepdf import Assist 


class operators_SetGrayStroke(Assist.BaseJavaClass):
    """!Class representing gray level for stroking operations."""

    java_class_name = "com.aspose.python.pdf.operators.SetGrayStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
