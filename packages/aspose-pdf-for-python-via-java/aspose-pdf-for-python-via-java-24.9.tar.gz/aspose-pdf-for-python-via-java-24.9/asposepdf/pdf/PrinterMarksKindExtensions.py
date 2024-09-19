import jpype 
from asposepdf import Assist 


class PrinterMarksKindExtensions(Assist.BaseJavaClass):
    """!Provides extension methods for the {@link PrinterMarksKind} enumeration."""

    java_class_name = "com.aspose.python.pdf.PrinterMarksKindExtensions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
