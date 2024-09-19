import jpype 
from asposepdf import Assist 


class EpubSaveOptions(Assist.BaseJavaClass):
    """!Save options for export to EPUB format"""

    java_class_name = "com.aspose.python.pdf.EpubSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
