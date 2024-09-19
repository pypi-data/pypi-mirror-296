import jpype 
from asposepdf import Assist 


class FreeTextAnnotation(Assist.BaseJavaClass):
    """!Represents a free text annotation that displays text directly on the page. Unlike an ordinary
     text annotation, a free text annotation has no open or closed state; instead of being displayed
     in a pop-up window, the text is always visible."""

    java_class_name = "com.aspose.python.pdf.FreeTextAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
