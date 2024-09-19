import jpype 
from asposepdf import Assist 


class plugins_pdftoimage_Jpeg(Assist.BaseJavaClass):
    """!Represents Pdf to Jpeg plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdftoimage.Jpeg"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
