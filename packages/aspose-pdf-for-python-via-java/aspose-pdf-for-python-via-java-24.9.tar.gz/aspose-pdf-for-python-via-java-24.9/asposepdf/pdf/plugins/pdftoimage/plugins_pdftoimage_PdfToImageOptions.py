import jpype 
from asposepdf import Assist 


class plugins_pdftoimage_PdfToImageOptions(Assist.BaseJavaClass):
    """!Represents options for the {@link PdfToImage} plugin.
     <hr>
     The PdfImageOptions class contains base functions to add data (files, streams) representing input PDF documents.
     </hr>"""

    java_class_name = "com.aspose.python.pdf.plugins.pdftoimage.PdfToImageOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
