import jpype 
from asposepdf import Assist 


class devices_TiffSettings(Assist.BaseJavaClass):
    """!This class represents settings for importing pdf to Tiff."""

    java_class_name = "com.aspose.python.pdf.devices.TiffSettings"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
