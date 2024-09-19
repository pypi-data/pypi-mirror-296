import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_FontEncodingRules(Assist.BaseJavaClass):
    """!This enumeration defines rules which tune encoding logic"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.FontEncodingRules"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DecreaseToUnicodePriorityLevel = 1
    _Default = 0
