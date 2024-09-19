import jpype 
from asposepdf import Assist 


class InvalidFormTypeOperationException(Assist.BaseJavaClass):
    """!The exception that is thrown when an operation with form type is not valid."""

    java_class_name = "com.aspose.python.pdf.InvalidFormTypeOperationException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
