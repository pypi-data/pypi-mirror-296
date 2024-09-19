import jpype 
from asposepdf import Assist 


class plugins_implementations_PdfConverterOptions(Assist.BaseJavaClass):
    """!Represents options for Pdf converter plugins."""

    java_class_name = "com.aspose.python.pdf.plugins.implementations.PdfConverterOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
