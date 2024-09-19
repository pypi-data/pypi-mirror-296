import jpype 
from asposepdf import Assist 


class HeaderFooter(Assist.BaseJavaClass):
    """!Class represents header or footer pdf page."""

    java_class_name = "com.aspose.python.pdf.HeaderFooter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
