import jpype 
from asposepdf import Assist 


class devices_JpegDevice(Assist.BaseJavaClass):
    """!Represents image device that helps to save pdf document pages into jpeg."""

    java_class_name = "com.aspose.python.pdf.devices.JpegDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
