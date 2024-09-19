import jpype 
from asposepdf import Assist 


class plugins_signature_SignOptions(Assist.BaseJavaClass):
    """!Represents Sign Options for {@link Signature} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.signature.SignOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
