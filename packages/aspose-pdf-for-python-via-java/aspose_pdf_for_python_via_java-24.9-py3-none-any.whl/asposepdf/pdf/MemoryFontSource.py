import jpype 
from asposepdf import Assist 


class MemoryFontSource(Assist.BaseJavaClass):
    """!Represents single font file source."""

    java_class_name = "com.aspose.python.pdf.MemoryFontSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
