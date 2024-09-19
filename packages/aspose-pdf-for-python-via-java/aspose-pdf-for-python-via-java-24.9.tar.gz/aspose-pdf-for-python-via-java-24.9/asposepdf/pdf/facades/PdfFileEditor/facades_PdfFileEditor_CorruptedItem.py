import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_CorruptedItem(Assist.BaseJavaClass):
    """!Class which provides information about corrupted files in time of concatenation."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.CorruptedItem"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
