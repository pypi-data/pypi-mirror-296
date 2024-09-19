import jpype 
from asposepdf import Assist 


class StrikeOutAnnotation(Assist.BaseJavaClass):
    """!Represents a strikeout annotation that appears as a strikeout in the text of the document."""

    java_class_name = "com.aspose.python.pdf.StrikeOutAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
