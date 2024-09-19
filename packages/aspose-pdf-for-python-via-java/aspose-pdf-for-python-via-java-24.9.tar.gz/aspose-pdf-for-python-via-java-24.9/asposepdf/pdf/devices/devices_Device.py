import jpype 
from asposepdf import Assist 


class devices_Device(Assist.BaseJavaClass):
    """!Abstract class for all types of devices. Device is used to represent pdf document in some format.
     For example, document page can be represented as image or text."""

    java_class_name = "com.aspose.python.pdf.devices.Device"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
