import jpype 
from asposepdf import Assist 


class MarginInfo(Assist.BaseJavaClass):
    """!This class represents a margin for different objects."""

    java_class_name = "com.aspose.python.pdf.MarginInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
