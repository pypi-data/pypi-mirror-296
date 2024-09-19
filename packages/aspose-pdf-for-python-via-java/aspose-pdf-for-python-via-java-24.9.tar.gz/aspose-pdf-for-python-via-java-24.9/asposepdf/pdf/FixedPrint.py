import jpype 
from asposepdf import Assist 


class FixedPrint(Assist.BaseJavaClass):
    """!Represent Fixed print data of Watermark Annotation."""

    java_class_name = "com.aspose.python.pdf.FixedPrint"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
