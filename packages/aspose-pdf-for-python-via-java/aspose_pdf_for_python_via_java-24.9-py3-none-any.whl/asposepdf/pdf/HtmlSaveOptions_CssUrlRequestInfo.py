import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_CssUrlRequestInfo(Assist.BaseJavaClass):
    """!Represents set of data that related to request from converter to custom code aimed to get
     desirable URL (or URL template)of subject CSS"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.CssUrlRequestInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
