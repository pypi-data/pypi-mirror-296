import jpype 
from asposepdf import Assist 


class XslFoLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading/importing XSL-FO file into pdf document."""

    java_class_name = "com.aspose.python.pdf.XslFoLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
