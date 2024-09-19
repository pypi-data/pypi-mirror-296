import jpype 
from asposepdf import Assist 


class operators_SetLineCap(Assist.BaseJavaClass):
    """!Class representing J operator (set line cap style)."""

    java_class_name = "com.aspose.python.pdf.operators.SetLineCap"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
