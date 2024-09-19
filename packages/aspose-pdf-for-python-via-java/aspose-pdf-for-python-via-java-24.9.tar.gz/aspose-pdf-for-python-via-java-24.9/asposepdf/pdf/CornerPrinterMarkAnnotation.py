import jpype 
from asposepdf import Assist 


class CornerPrinterMarkAnnotation(Assist.BaseJavaClass):
    """!Represents annotation types that are placed in the corners of the printed page."""

    java_class_name = "com.aspose.python.pdf.CornerPrinterMarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
