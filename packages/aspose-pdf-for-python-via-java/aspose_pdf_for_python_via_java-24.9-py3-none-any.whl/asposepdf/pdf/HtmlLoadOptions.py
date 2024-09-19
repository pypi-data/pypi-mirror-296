import jpype 
from asposepdf import Assist 


class HtmlLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading/importing html file into pdf document."""

    java_class_name = "com.aspose.python.pdf.HtmlLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
