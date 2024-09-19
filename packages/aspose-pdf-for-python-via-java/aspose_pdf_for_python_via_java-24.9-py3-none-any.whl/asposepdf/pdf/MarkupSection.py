import jpype 
from asposepdf import Assist 


class MarkupSection(Assist.BaseJavaClass):
    """!Represents a markup section - the rectangular region of a page that contains text and can be visually divided from another text blocks."""

    java_class_name = "com.aspose.python.pdf.MarkupSection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
