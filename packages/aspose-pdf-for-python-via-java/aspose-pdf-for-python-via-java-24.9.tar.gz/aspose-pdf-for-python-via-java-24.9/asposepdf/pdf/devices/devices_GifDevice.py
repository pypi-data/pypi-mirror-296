import jpype 
from asposepdf import Assist 


class devices_GifDevice(Assist.BaseJavaClass):
    """!Represents image device that helps to save pdf document pages into gif."""

    java_class_name = "com.aspose.python.pdf.devices.GifDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
