import jpype 
from asposepdf import Assist 


class TextBuilder(Assist.BaseJavaClass):
    """!Appends text object to Pdf page."""

    java_class_name = "com.aspose.python.pdf.TextBuilder"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
