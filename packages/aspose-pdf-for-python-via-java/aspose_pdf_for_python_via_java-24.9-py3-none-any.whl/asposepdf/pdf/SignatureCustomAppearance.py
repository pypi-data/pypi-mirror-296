import jpype 
from asposepdf import Assist 


class SignatureCustomAppearance(Assist.BaseJavaClass):
    """!An abstract class which represents signature custon appearance object."""

    java_class_name = "com.aspose.python.pdf.SignatureCustomAppearance"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
