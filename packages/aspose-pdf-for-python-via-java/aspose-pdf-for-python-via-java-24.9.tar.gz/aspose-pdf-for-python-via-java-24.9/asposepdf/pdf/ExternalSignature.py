import jpype 
from asposepdf import Assist 


class ExternalSignature(Assist.BaseJavaClass):
    """!Creates a detached PKCS#7Detached signature using a X509Certificate2. It supports usb smartcards, tokens without exportable private keys."""

    java_class_name = "com.aspose.python.pdf.ExternalSignature"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
