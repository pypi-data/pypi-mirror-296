import jpype 
from asposepdf import Assist 


class plugins_pdfhtml_PdfToHtmlOptions_SaveDataType(Assist.BaseJavaClass):
    """!Defines output type of HTML file."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfhtml.PdfToHtmlOptions.SaveDataType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _FileWithEmbeddedResources = 1
    _StreamWithEmbeddedResources = 2
    _FileWithExternalResources = 0
