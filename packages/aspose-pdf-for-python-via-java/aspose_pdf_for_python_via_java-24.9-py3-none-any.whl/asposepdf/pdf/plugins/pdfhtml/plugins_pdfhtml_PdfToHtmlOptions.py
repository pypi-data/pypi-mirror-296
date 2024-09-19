import jpype 
from asposepdf import Assist 


class plugins_pdfhtml_PdfToHtmlOptions(Assist.BaseJavaClass):
    """!Represents PDF to HTML converter options for {@link PdfHtml} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfhtml.PdfToHtmlOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
