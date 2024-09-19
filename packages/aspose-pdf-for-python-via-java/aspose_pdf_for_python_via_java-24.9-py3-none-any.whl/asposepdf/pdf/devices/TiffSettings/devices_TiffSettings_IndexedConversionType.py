import jpype 
from asposepdf import Assist 


class devices_TiffSettings_IndexedConversionType(Assist.BaseJavaClass):
    """!Class represented indexed conversion types"""

    java_class_name = "com.aspose.python.pdf.devices.TiffSettings.IndexedConversionType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Pixelated = 1
    _Simple = 0
