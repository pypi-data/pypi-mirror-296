import jpype 
from asposepdf import Assist 


class EncryptedPayload(Assist.BaseJavaClass):
    """!Represents encrypted payload in file specification."""

    java_class_name = "com.aspose.python.pdf.EncryptedPayload"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
