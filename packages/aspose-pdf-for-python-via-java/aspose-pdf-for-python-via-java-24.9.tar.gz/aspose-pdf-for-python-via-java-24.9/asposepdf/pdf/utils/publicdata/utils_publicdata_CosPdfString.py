import jpype 
from asposepdf import Assist 


class utils_publicdata_CosPdfString(Assist.BaseJavaClass):
    """!This class represents Pdf String object."""

    java_class_name = "com.aspose.python.pdf.utils.publicdata.CosPdfString"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
