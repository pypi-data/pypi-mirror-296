import jpype 
from asposepdf import Assist 


class LinkAnnotation(Assist.BaseJavaClass):
    """!Represents either a hypertext link to a destination elsewhere in the document or an action to be
     performed."""

    java_class_name = "com.aspose.python.pdf.LinkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
