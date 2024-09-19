import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_HtmlImageSavingInfo(Assist.BaseJavaClass):
    """!This class represents set of data that related to external resource image file's saving
     during PDF to HTML conversion."""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.HtmlImageSavingInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
