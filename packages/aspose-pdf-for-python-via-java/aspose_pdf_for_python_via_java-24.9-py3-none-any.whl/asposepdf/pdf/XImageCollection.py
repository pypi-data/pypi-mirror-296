import jpype 
from asposepdf import Assist 


class XImageCollection(Assist.BaseJavaClass):
    """!Class representing XImage collection."""

    java_class_name = "com.aspose.python.pdf.XImageCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
