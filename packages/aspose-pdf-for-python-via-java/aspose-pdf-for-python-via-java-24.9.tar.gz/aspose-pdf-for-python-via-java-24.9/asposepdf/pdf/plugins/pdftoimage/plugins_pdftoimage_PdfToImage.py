import jpype 
from asposepdf import Assist 


class plugins_pdftoimage_PdfToImage(Assist.BaseJavaClass):
    """!Represents PdfImage plugin.
     <hr>
     The {@link PdfToImage} class is used to convert PDF document to images (Jpeg).
     </hr>"""

    java_class_name = "com.aspose.python.pdf.plugins.pdftoimage.PdfToImage"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
