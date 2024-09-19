import jpype 
from asposepdf import Assist 


class CgmLoadOptions(Assist.BaseJavaClass):
    """!Contains options for loading/importing CGM file into pdf document."""

    java_class_name = "com.aspose.python.pdf.CgmLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
