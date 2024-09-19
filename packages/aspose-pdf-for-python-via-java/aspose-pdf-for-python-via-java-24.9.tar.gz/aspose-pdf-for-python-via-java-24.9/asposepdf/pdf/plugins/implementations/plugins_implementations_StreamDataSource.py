import jpype 
from asposepdf import Assist 


class plugins_implementations_StreamDataSource(Assist.BaseJavaClass):
    """!Represents stream data source for load and save operations of a plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.implementations.StreamDataSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
