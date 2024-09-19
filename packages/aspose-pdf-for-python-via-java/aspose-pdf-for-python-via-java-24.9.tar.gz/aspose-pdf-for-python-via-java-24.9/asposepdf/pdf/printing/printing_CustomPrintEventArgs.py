import jpype 
from asposepdf import Assist 


class printing_CustomPrintEventArgs(Assist.BaseJavaClass):
    """!Provides data for the  PdfViewer.getCustomPrintDelegate() event."""

    java_class_name = "com.aspose.python.pdf.printing.CustomPrintEventArgs"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

