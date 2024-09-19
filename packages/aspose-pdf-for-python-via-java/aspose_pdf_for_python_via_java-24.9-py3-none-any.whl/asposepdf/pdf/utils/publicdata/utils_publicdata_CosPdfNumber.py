import jpype 
from asposepdf import Assist 


class utils_publicdata_CosPdfNumber(Assist.BaseJavaClass):
    """!This class represents Pdf Number type."""

    java_class_name = "com.aspose.python.pdf.utils.publicdata.CosPdfNumber"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
