import jpype 
from asposepdf import Assist 


class devices_DocumentDevice(Assist.BaseJavaClass):
    """!Abstract class for all devices which is used to process the whole pdf document."""

    java_class_name = "com.aspose.python.pdf.devices.DocumentDevice"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
