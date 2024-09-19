import jpype 
from asposepdf import Assist 


class devices_Resolution(Assist.BaseJavaClass):
    """!Represents class for holding image resolution."""

    java_class_name = "com.aspose.python.pdf.devices.Resolution"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
