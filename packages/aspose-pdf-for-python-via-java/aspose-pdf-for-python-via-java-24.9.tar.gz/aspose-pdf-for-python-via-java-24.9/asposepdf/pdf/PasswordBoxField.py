import jpype 
from asposepdf import Assist 


class PasswordBoxField(Assist.BaseJavaClass):
    """!Class descibes text field for entering password."""

    java_class_name = "com.aspose.python.pdf.PasswordBoxField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
