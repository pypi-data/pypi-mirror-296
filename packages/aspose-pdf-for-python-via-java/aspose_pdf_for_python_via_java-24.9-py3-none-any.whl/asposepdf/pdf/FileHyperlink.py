import jpype 
from asposepdf import Assist 


class FileHyperlink(Assist.BaseJavaClass):
    """!Represents file hyperlink object."""

    java_class_name = "com.aspose.python.pdf.FileHyperlink"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
