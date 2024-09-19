import jpype 
from asposepdf import Assist 


class plugins_pdfdoc_SaveFormat(Assist.BaseJavaClass):
    """!Allows to specify .doc or .docx file format."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfdoc.SaveFormat"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DocX = 1
    _Doc = 0
