import jpype 
from asposepdf import Assist 


class XmlLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading/importing XML file into pdf document."""

    java_class_name = "com.aspose.python.pdf.XmlLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
