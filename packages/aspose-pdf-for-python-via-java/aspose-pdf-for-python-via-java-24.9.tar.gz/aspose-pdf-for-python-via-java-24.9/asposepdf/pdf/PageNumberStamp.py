import jpype 
from asposepdf import Assist 


class PageNumberStamp(Assist.BaseJavaClass):
    """!Represents page number stamp and used to number pages."""

    java_class_name = "com.aspose.python.pdf.PageNumberStamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
