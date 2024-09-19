import jpype 
from asposepdf import Assist 


class utils_publicdata_CosPdfPrimitive(Assist.BaseJavaClass):
    """!This class represents base public type {@link CosPdfPrimitive}."""

    java_class_name = "com.aspose.python.pdf.utils.publicdata.CosPdfPrimitive"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
