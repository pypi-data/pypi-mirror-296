import jpype 
from asposepdf import Assist 


class exceptions_NotImplementedException(Assist.BaseJavaClass):
    """!The exception that is thrown when a requested method or operation is not implemented."""

    java_class_name = "com.aspose.python.pdf.exceptions.NotImplementedException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
