import jpype 
from asposepdf import Assist 


class printing_PdfPrinterSettings(Assist.BaseJavaClass):
    """!Specifies information about how a document is printed, including the printer that prints it."""

    java_class_name = "com.aspose.python.pdf.printing.PdfPrinterSettings"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
