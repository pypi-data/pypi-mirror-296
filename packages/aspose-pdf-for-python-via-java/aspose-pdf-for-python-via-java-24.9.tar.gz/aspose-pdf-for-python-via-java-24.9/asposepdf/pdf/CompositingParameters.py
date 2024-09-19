import jpype 
from asposepdf import Assist 


class CompositingParameters(Assist.BaseJavaClass):
    """!Represents an object containing graphics compositing parameters of current graphics state."""

    java_class_name = "com.aspose.python.pdf.CompositingParameters"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
