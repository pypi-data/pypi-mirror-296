import jpype 
from asposepdf import Assist 


class printing_PdfPrinterResolution(Assist.BaseJavaClass):
    """!Represents the resolution supported by a printer."""

    java_class_name = "com.aspose.python.pdf.printing.PdfPrinterResolution"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
