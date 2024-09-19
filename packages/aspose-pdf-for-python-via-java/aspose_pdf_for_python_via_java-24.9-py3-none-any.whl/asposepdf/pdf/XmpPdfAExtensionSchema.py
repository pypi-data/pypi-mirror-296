import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionSchema(Assist.BaseJavaClass):
    """!Describes the XMP extension schema which is provided by PDF/A-1."""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionSchema"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

