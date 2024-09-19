import jpype 
from asposepdf import Assist 


class plugins_pdfhtml_HtmlToPdfOptions(Assist.BaseJavaClass):
    """!Represents HTML to PDF converter options for {@link PdfHtml} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfhtml.HtmlToPdfOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
