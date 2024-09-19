import jpype 
from asposepdf import Assist 


class printing_PdfPrintRange(Assist.BaseJavaClass):
    """!Specifies the part of the document to print."""

    java_class_name = "com.aspose.python.pdf.printing.PdfPrintRange"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

