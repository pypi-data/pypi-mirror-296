import jpype 
from asposepdf import Assist 


class RenditionType(Assist.BaseJavaClass):
    """!Enumeration describes possible types of Rendition."""

    java_class_name = "com.aspose.python.pdf.RenditionType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Undefined = 2
    _Media = 0
    _Selector = 1
