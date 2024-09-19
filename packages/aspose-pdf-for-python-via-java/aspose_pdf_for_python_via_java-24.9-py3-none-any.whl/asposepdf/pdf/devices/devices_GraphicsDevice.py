import jpype 
from asposepdf import Assist 


class devices_GraphicsDevice(Assist.BaseJavaClass):
    """!Represents image device that helps to render pdf document pages into graphics."""

    java_class_name = "com.aspose.python.pdf.devices.GraphicsDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
