import jpype 
from asposepdf import Assist 


class WarningCallback(Assist.BaseJavaClass):
    """!Interface for user's callback mechanism support."""

    java_class_name = "com.aspose.python.pdf.WarningCallback"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
