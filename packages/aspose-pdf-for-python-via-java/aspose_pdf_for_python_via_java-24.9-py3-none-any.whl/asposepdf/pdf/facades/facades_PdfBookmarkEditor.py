import jpype 
from asposepdf import Assist 


class facades_PdfBookmarkEditor(Assist.BaseJavaClass):
    """!Represents a class to work with PDF file's bookmarks including create, modify, export, import and
     delete."""

    java_class_name = "com.aspose.python.pdf.facades.PdfBookmarkEditor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
