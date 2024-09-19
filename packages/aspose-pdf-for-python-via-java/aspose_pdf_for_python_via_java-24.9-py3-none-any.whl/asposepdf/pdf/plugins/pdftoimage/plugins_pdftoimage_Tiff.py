import jpype 
from asposepdf import Assist 


class plugins_pdftoimage_Tiff(Assist.BaseJavaClass):
    """!Represents Pdf to Tiff plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdftoimage.Tiff"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
