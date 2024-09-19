import jpype 
from asposepdf import Assist 


class OcspSettings(Assist.BaseJavaClass):
    """!Represents the ocsp settings using during signing process."""

    java_class_name = "com.aspose.python.pdf.OcspSettings"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
