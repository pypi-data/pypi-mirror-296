import jpype 
from asposepdf import Assist 


class plugins_security_EncryptionOptions(Assist.BaseJavaClass):
    """!Represents Encryption Options for {@link Security} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.security.EncryptionOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
