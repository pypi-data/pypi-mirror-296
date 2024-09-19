import jpype 
from asposepdf import Assist 


class MdLoadOptions(Assist.BaseJavaClass):
    """!Load options for Markdown format conversion."""

    java_class_name = "com.aspose.python.pdf.MdLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
