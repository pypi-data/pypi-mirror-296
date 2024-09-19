import jpype 
from asposepdf import Assist 


class PdfXmlLoadOptions(Assist.BaseJavaClass):
    """!Load options for PdfXml format."""

    java_class_name = "com.aspose.python.pdf.PdfXmlLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
