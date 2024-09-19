import jpype 
from asposepdf import Assist 


class RenditionAction(Assist.BaseJavaClass):
    """!A rendition action that controls the playing of multimedia content."""

    java_class_name = "com.aspose.python.pdf.RenditionAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
