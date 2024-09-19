import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_ConcatenationProgressHandler(Assist.BaseJavaClass):
    """!Represents class with abstract method that usually supplied by calling side and handles
     progress events that comes from concatenation. Usually such supplied customer's handler can
     be used to show total concatenation progress on console or in progress bar.
     represents information about occurred progress event"""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.ConcatenationProgressHandler"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
