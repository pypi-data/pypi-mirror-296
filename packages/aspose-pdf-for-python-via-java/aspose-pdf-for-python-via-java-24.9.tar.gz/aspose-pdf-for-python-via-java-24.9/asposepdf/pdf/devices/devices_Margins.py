import jpype 
from asposepdf import Assist 


class devices_Margins(Assist.BaseJavaClass):
    """!This class represents margins of an image."""

    java_class_name = "com.aspose.python.pdf.devices.Margins"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
