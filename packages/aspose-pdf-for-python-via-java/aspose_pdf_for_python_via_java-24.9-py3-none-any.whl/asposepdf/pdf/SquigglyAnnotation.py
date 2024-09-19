import jpype 
from asposepdf import Assist 


class SquigglyAnnotation(Assist.BaseJavaClass):
    """!Represents the squiggly annotation that appears as a jagged underline in the text of a document."""

    java_class_name = "com.aspose.python.pdf.SquigglyAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
