import jpype 
from asposepdf import Assist 


class PrinterMarkAnnotation(Assist.BaseJavaClass):
    """!Abstract class representing printer mark annotation."""

    java_class_name = "com.aspose.python.pdf.PrinterMarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
