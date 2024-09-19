import jpype 
from asposepdf import Assist 


class utils_publicdata_CosPdfBoolean(Assist.BaseJavaClass):
    """!This class represents boolean type."""

    java_class_name = "com.aspose.python.pdf.utils.publicdata.CosPdfBoolean"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
