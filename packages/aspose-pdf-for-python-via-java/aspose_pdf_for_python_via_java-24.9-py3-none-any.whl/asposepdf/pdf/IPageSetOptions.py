import jpype 
from asposepdf import Assist 


class IPageSetOptions(Assist.BaseJavaClass):
    """!Defines conversion options related to a set of pages to convert."""

    java_class_name = "com.aspose.python.pdf.IPageSetOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
