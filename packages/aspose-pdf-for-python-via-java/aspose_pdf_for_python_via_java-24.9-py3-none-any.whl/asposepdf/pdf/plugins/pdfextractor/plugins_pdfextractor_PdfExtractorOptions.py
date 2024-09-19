import jpype 
from asposepdf import Assist 


class plugins_pdfextractor_PdfExtractorOptions(Assist.BaseJavaClass):
    """!Represents options for the PdfExtractor plugin.
     <hr>
     The {@link PdfExtractorOptions} contains base functions to add data (files, streams) representing input PDF documents.
     Please create PdfExtractorToTextOptions or PdfExtractorToTextOptions instead of this.
     </hr>"""

    java_class_name = "com.aspose.python.pdf.plugins.pdfextractor.PdfExtractorOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
