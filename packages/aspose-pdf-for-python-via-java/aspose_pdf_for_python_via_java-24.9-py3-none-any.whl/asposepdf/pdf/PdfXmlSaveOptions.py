import jpype 
from asposepdf import Assist 


class PdfXmlSaveOptions(Assist.BaseJavaClass):
    """!Save options for PdfXml format."""

    java_class_name = "com.aspose.python.pdf.PdfXmlSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
