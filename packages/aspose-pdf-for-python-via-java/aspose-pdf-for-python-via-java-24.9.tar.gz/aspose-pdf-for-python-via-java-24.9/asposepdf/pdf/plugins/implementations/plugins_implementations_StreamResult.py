import jpype 
from asposepdf import Assist 


class plugins_implementations_StreamResult(Assist.BaseJavaClass):
    """!Represents operation result in the form of Stream."""

    java_class_name = "com.aspose.python.pdf.plugins.implementations.StreamResult"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
