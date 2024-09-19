import jpype 
from asposepdf import Assist 


class Page(Assist.BaseJavaClass):
    """!Class representing page of PDF document."""

    java_class_name = "com.aspose.python.pdf.Page"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
