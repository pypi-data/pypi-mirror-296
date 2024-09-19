import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionSchemaDescription(Assist.BaseJavaClass):
    """!Represents the description of XMP extension schema which is provided by PDF/A-1."""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionSchemaDescription"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
