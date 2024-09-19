import jpype 
from asposepdf import Assist 


class devices_ThumbnailDevice(Assist.BaseJavaClass):
    """!Represents image device that save pdf document pages into Thumbnail image."""

    java_class_name = "com.aspose.python.pdf.devices.ThumbnailDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
