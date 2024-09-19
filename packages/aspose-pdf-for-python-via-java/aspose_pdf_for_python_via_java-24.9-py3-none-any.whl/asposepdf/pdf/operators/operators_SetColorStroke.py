import jpype 
from asposepdf import Assist 


class operators_SetColorStroke(Assist.BaseJavaClass):
    """!Class representing SC operator set color for stroking color operators."""

    java_class_name = "com.aspose.python.pdf.operators.SetColorStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
