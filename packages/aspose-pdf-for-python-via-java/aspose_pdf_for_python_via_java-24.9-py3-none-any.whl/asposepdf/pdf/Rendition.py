import jpype 
from asposepdf import Assist 


class Rendition(Assist.BaseJavaClass):
    """!Class which describes rendition object of RendtionAnnotation."""

    java_class_name = "com.aspose.python.pdf.Rendition"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
