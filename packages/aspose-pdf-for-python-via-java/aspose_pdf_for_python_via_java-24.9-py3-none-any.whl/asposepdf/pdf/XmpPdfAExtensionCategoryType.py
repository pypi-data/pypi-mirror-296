import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionCategoryType(Assist.BaseJavaClass):
    """!Property category: internal or external."""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionCategoryType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Internal = 0
    _External = 1
