import jpype 
from asposepdf import Assist 


class exceptions_IndexOutOfRangeException(Assist.BaseJavaClass):
    """!Represents Index Out Of Range errors that occur during PDF application execution."""

    java_class_name = "com.aspose.python.pdf.exceptions.IndexOutOfRangeException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
