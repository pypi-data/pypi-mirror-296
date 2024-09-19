import jpype 
from asposepdf import Assist 


class plugins_ResultContainer(Assist.BaseJavaClass):
    """!Represents container that contains the result collection of processing the plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.ResultContainer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
