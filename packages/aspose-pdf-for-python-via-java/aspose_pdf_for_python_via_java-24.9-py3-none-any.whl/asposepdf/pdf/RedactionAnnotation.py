import jpype 
from asposepdf import Assist 


class RedactionAnnotation(Assist.BaseJavaClass):
    """!Represents Redact annotation."""

    java_class_name = "com.aspose.python.pdf.RedactionAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
