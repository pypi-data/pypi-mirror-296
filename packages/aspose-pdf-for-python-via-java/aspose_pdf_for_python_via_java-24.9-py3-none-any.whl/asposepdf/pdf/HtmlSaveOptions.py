import jpype 
from asposepdf import Assist 


class HtmlSaveOptions(Assist.BaseJavaClass):
    """!Save options for export to Html format"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
