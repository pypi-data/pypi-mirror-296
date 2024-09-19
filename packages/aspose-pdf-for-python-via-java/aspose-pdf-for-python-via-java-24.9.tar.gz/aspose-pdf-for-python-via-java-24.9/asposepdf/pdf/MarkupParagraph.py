import jpype 
from asposepdf import Assist 


class MarkupParagraph(Assist.BaseJavaClass):
    """!Represents a paragraph."""

    java_class_name = "com.aspose.python.pdf.MarkupParagraph"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
