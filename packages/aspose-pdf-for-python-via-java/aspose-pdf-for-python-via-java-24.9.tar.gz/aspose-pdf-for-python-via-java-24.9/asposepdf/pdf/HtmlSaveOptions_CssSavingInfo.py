import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_CssSavingInfo(Assist.BaseJavaClass):
    """!This class represents set of data that related to custom saving of CSS during conversion of
     PDF to HTML format"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.CssSavingInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
