import jpype 
from asposepdf import Assist 


class PclLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading(import) PCL file into pdf document."""

    java_class_name = "com.aspose.python.pdf.PclLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
