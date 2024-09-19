import jpype 
from asposepdf import Assist 


class printing_PdfPrinterResolutionKind(Assist.BaseJavaClass):
    """!Specifies a printer resolution."""

    java_class_name = "com.aspose.python.pdf.printing.PdfPrinterResolutionKind"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

