import jpype 
from asposepdf import Assist 


class PdfActionCollection(Assist.BaseJavaClass):
    """!Class describes list of actions."""

    java_class_name = "com.aspose.python.pdf.PdfActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
