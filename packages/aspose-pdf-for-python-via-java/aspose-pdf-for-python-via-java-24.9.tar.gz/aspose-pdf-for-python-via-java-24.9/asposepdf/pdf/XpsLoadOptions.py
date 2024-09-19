import jpype 
from asposepdf import Assist 


class XpsLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading/importing xps file into pdf document."""

    java_class_name = "com.aspose.python.pdf.XpsLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
