import jpype 
from asposepdf import Assist 


class utils_publicdata_ICosPdfPrimitive(Assist.BaseJavaClass):
    """!Interface for work with PDF data entity"""

    java_class_name = "com.aspose.python.pdf.utils.publicdata.ICosPdfPrimitive"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
