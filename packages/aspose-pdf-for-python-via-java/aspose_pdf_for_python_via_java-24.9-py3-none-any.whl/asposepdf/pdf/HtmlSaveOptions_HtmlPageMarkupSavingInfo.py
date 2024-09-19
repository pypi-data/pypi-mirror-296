import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_HtmlPageMarkupSavingInfo(Assist.BaseJavaClass):
    """!If SplitToPages property of HtmlSaveOptions, then several HTML-files (one HTML file per
     converted page) are created during conversion of PDF to HTML. This class represents set of
     data that related to custom saving of one HTML-page's markup during conversion of PDF to HTML"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.HtmlPageMarkupSavingInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
