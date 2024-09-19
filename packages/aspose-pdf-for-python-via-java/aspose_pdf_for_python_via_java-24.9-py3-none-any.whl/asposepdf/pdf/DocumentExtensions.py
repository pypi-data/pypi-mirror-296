import jpype 
from asposepdf import Assist 


class DocumentExtensions(Assist.BaseJavaClass):
    """!Provides additional capabilities for the Document class."""

    java_class_name = "com.aspose.python.pdf.DocumentExtensions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
