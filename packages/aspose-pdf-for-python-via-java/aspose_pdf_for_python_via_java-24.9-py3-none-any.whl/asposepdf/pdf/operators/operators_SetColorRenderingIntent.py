import jpype 
from asposepdf import Assist 


class operators_SetColorRenderingIntent(Assist.BaseJavaClass):
    """!Class representing ri operator (set color rendering intent)."""

    java_class_name = "com.aspose.python.pdf.operators.SetColorRenderingIntent"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
