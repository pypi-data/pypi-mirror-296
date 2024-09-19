import jpype 
from asposepdf import Assist 


class BuildVersionInfo(Assist.BaseJavaClass):
    """!This class provides information about current product build."""

    java_class_name = "com.aspose.python.pdf.BuildVersionInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

