import jpype 
from asposepdf import Assist 


class operators_ClosePathEOFillStroke(Assist.BaseJavaClass):
    """!Class representing b* operator (close, fill and stroke path using even-odd rule)."""

    java_class_name = "com.aspose.python.pdf.operators.ClosePathEOFillStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
