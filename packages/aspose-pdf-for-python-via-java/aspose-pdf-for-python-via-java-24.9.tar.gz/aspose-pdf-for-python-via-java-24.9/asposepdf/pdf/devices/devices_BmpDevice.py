import jpype 
from asposepdf import Assist 


class devices_BmpDevice(Assist.BaseJavaClass):
    """!Represents image device that helps to save pdf document pages into bmp."""

    java_class_name = "com.aspose.python.pdf.devices.BmpDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
