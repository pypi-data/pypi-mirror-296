import jpype 
from asposepdf import Assist 


class facades_PdfPrintPageInfo(Assist.BaseJavaClass):
    """!Represents an object that contains current printing page info."""

    java_class_name = "com.aspose.python.pdf.facades.PdfPrintPageInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
