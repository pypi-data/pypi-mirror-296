import jpype 
from asposepdf import Assist 


class exceptions_TaggedException(Assist.BaseJavaClass):
    """!Represents exception for TaggedPDF content of document."""

    java_class_name = "com.aspose.python.pdf.exceptions.TaggedException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
