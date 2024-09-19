import jpype 
from asposepdf import Assist 


class plugins_pdfa_PdfAConvertOptions(Assist.BaseJavaClass):
    """!Represents options for converting PDF documents to PDF/A format with the {@link PdfAConverter} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfa.PdfAConvertOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
