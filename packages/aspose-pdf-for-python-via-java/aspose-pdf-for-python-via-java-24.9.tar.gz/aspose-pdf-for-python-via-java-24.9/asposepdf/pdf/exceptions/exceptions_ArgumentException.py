import jpype 
from asposepdf import Assist 


class exceptions_ArgumentException(Assist.BaseJavaClass):
    """!The exception that is thrown when one of the arguments provided to a method is not valid."""

    java_class_name = "com.aspose.python.pdf.exceptions.ArgumentException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
