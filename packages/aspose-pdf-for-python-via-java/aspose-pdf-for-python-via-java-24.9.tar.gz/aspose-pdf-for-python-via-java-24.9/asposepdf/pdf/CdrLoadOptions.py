import jpype 
from asposepdf import Assist 


class CdrLoadOptions(Assist.BaseJavaClass):
    """!Class describes CDR load options."""

    java_class_name = "com.aspose.python.pdf.CdrLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
