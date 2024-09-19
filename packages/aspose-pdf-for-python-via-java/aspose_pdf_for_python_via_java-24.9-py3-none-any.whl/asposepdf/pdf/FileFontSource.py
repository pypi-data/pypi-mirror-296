import jpype 
from asposepdf import Assist 


class FileFontSource(Assist.BaseJavaClass):
    """!Represents single font file source."""

    java_class_name = "com.aspose.python.pdf.FileFontSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
