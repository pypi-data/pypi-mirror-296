import jpype 
from asposepdf import Assist 


class SignHash(Assist.BaseJavaClass):
    """!Delegate for custom sign the document hash (Beta)."""

    java_class_name = "com.aspose.python.pdf.SignHash"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
