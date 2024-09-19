import jpype 
from asposepdf import Assist 


class PdfPageStamp(Assist.BaseJavaClass):
    """!Class represents stamp which uses PDF page as stamp."""

    java_class_name = "com.aspose.python.pdf.PdfPageStamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
