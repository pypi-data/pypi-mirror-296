import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_AntialiasingProcessingType(Assist.BaseJavaClass):
    """!This enum describes possible antialiasing measures during conversion"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.AntialiasingProcessingType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _TryCorrectResultHtml = 1
    _NoAdditionalProcessing = 0
