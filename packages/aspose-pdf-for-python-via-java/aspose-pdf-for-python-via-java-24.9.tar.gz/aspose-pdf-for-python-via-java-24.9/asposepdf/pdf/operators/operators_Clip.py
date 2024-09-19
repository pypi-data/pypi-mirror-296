import jpype 
from asposepdf import Assist 


class operators_Clip(Assist.BaseJavaClass):
    """!Class representing W operator (set clipping path using non-zero winding rule)."""

    java_class_name = "com.aspose.python.pdf.operators.Clip"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
