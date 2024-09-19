import jpype 
from asposepdf import Assist 


class FolderFontSource(Assist.BaseJavaClass):
    """!Represents the folder that contains font files."""

    java_class_name = "com.aspose.python.pdf.FolderFontSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
