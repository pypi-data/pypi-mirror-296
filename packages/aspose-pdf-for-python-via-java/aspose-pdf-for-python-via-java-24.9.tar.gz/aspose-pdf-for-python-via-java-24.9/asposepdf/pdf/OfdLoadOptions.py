import jpype 
from asposepdf import Assist 


class OfdLoadOptions(Assist.BaseJavaClass):
    """!Load options for OFD format."""

    java_class_name = "com.aspose.python.pdf.OfdLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
