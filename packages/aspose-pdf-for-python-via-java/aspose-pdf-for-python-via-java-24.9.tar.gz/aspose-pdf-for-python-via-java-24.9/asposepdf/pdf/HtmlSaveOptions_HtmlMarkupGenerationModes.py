import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_HtmlMarkupGenerationModes(Assist.BaseJavaClass):
    """!Sometimes specific reqirments to created HTML are present. This enum defines HTML preparing
     modes that can be used during conversion of PDF to HTML to match such specific requirments."""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.HtmlMarkupGenerationModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _WriteAllHtml = 0
    _WriteOnlyBodyContent = 1
