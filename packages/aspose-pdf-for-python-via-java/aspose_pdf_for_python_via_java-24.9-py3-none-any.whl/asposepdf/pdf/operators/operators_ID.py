import jpype 
from asposepdf import Assist 


class operators_ID(Assist.BaseJavaClass):
    """!Class representing ID operator (Begin inline image data)."""

    java_class_name = "com.aspose.python.pdf.operators.ID"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
