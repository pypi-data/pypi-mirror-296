import jpype 
from asposepdf import Assist 


class FileParams(Assist.BaseJavaClass):
    """!Defines an embedded file parameter dictionary that shall contain additional file-specific
     information."""

    java_class_name = "com.aspose.python.pdf.FileParams"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
