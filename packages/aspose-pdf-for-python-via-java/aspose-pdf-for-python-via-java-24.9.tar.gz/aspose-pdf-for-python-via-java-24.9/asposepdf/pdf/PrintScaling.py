import jpype 
from asposepdf import Assist 


class PrintScaling(Assist.BaseJavaClass):
    """!The page scaling option that shall be selected when a print dialog is displayed for this document."""

    java_class_name = "com.aspose.python.pdf.PrintScaling"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _AppDefault = 0
    _None = 1
