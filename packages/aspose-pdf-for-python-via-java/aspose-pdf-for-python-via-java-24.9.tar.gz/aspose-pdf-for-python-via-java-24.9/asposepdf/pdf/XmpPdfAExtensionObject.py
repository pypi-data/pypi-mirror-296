import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionObject(Assist.BaseJavaClass):
    """!Represents the base class for field, property, value type instances."""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionObject"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
