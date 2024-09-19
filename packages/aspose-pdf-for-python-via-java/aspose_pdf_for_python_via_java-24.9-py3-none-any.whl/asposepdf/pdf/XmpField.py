import jpype 
from asposepdf import Assist 


class XmpField(Assist.BaseJavaClass):
    """!Represents XMP field."""

    java_class_name = "com.aspose.python.pdf.XmpField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
