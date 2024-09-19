import jpype 
from asposepdf import Assist 


class HighlightAnnotation(Assist.BaseJavaClass):
    """!Represents a highlight annotation that highlights a range of text in the document."""

    java_class_name = "com.aspose.python.pdf.HighlightAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
