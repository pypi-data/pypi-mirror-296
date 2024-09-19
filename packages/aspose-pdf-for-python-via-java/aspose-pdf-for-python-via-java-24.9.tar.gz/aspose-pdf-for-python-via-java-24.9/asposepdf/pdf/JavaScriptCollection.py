import jpype 
from asposepdf import Assist 


class JavaScriptCollection(Assist.BaseJavaClass):
    """!This class represents collection of JavaScript."""

    java_class_name = "com.aspose.python.pdf.JavaScriptCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
