import jpype 
from asposepdf import Assist 


class XfdfWriter(Assist.BaseJavaClass):
    """!Aggregates methods of writing annotations and fields to XFDF file format"""

    java_class_name = "com.aspose.python.pdf.XfdfWriter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
