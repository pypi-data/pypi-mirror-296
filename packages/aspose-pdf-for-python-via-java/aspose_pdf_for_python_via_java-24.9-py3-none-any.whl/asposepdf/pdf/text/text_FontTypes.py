import jpype 
from asposepdf import Assist 


class text_FontTypes(Assist.BaseJavaClass):
    """!Supported font types enumeration."""

    java_class_name = "com.aspose.python.pdf.text.FontTypes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

