import jpype 
from asposepdf import Assist 


class exceptions_PdfOutOfMemoryException(Assist.BaseJavaClass):
    """!Represents OutOfMemory errors that occur during PDF application execution."""

    java_class_name = "com.aspose.python.pdf.exceptions.PdfOutOfMemoryException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
