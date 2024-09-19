import jpype 
from asposepdf import Assist 


class plugins_DataType(Assist.BaseJavaClass):
    """!Represents possible types of data for plugin processing."""

    java_class_name = "com.aspose.python.pdf.plugins.DataType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Stream = 1
    _File = 0
