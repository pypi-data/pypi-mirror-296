import jpype 
from asposepdf import Assist 


class EpubLoadOptions(Assist.BaseJavaClass):
    """!Contains options for loading/importing EPUB file into pdf document."""

    java_class_name = "com.aspose.python.pdf.EpubLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
