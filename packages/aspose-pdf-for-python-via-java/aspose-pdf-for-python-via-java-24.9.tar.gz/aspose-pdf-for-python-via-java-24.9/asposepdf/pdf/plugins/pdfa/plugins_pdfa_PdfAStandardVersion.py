import jpype 
from asposepdf import Assist 


class plugins_pdfa_PdfAStandardVersion(Assist.BaseJavaClass):
    """!Specifies the PDF/A standard version for a PDF document."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfa.PdfAStandardVersion"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Auto = 0
    _PDF_A_2A = 3
    _PDF_A_3B = 7
    _PDF_A_1A = 1
    _PDF_A_2B = 4
    _PDF_A_3A = 6
    _PDF_A_2U = 5
    _PDF_A_1B = 2
    _PDF_A_3U = 8
