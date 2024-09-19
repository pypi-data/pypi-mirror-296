import jpype 
from asposepdf import Assist 


class plugins_pdfxls_PdfToXlsOptions(Assist.BaseJavaClass):
    """!Represents PDF to XLSX converter options for {@link PdfXls} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfxls.PdfToXlsOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
