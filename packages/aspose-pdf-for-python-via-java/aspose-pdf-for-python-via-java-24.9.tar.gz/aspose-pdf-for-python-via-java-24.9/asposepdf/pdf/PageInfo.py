import jpype 
from asposepdf import Assist 


class PageInfo(Assist.BaseJavaClass):
    """!Represents the page information for pdf generator."""

    java_class_name = "com.aspose.python.pdf.PageInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
