import jpype 
from asposepdf import Assist 


class IPipelineOptions(Assist.BaseJavaClass):
    """!Defines conversion options related to pipeline configuration."""

    java_class_name = "com.aspose.python.pdf.IPipelineOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
