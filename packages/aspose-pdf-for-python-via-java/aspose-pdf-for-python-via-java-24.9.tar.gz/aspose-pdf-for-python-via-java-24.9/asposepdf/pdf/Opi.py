import jpype 
from asposepdf import Assist 


class Opi(Assist.BaseJavaClass):
    """!Represents The Open Prepress Interface (OPI) is a mechanism for creating low-resolution
     placeholders, or proxies, for such high-resolution images."""

    java_class_name = "com.aspose.python.pdf.Opi"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
