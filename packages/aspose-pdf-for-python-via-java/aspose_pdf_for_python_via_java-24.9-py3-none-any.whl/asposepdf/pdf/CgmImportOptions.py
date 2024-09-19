import jpype 
from asposepdf import Assist 


class CgmImportOptions(Assist.BaseJavaClass):
    """!Import option for import from Computer Graphics Metafile(CGM) format."""

    java_class_name = "com.aspose.python.pdf.CgmImportOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
