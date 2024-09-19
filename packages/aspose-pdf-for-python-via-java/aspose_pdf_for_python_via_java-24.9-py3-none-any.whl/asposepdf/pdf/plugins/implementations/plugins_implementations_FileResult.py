import jpype 
from asposepdf import Assist 


class plugins_implementations_FileResult(Assist.BaseJavaClass):
    """!Represents operation result in the form of string path to file."""

    java_class_name = "com.aspose.python.pdf.plugins.implementations.FileResult"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
