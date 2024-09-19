import jpype 
from asposepdf import Assist 


class XmpFieldType(Assist.BaseJavaClass):
    """!This enum represents types of a XMP field."""

    java_class_name = "com.aspose.python.pdf.XmpFieldType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Array = 1
    _Packet = 3
    _Unknown = 4
    _Property = 2
    _Struct = 0
