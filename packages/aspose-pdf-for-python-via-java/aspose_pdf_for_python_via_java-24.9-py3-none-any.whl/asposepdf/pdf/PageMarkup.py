import jpype 
from asposepdf import Assist 


class PageMarkup(Assist.BaseJavaClass):
    """!Page markup represented by collections of {@code MarkupSection} and {@code MarkupParagraph}."""

    java_class_name = "com.aspose.python.pdf.PageMarkup"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
