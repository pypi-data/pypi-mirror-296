import jpype 
from asposepdf import Assist 


class exceptions_JavascriptExtensionsException(Assist.BaseJavaClass):
    """!The exception that is thrown on errors when working with JavascriptExtensions."""

    java_class_name = "com.aspose.python.pdf.exceptions.JavascriptExtensionsException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
