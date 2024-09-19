import jpype 
from asposepdf import Assist 


class TextAnnotation(Assist.BaseJavaClass):
    """!Represents a text annotation that is a "sticky note" attached to a point in the PDF document."""

    java_class_name = "com.aspose.python.pdf.TextAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
