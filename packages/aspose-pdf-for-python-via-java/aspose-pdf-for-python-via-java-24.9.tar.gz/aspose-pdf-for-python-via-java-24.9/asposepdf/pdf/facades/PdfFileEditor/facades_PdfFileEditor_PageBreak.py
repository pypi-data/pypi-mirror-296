import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_PageBreak(Assist.BaseJavaClass):
    """!Data of page break position."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.PageBreak"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
