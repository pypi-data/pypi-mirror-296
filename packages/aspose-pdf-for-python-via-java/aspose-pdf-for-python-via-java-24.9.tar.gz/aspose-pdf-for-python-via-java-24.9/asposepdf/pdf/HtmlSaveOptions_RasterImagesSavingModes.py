import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_RasterImagesSavingModes(Assist.BaseJavaClass):
    """!Converted PDF can contain raster images(.png, *.jpeg etc.) This enum defines methods of how
     raster images can be handled during conversion of PDF to HTML"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.RasterImagesSavingModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _AsEmbeddedPartsOfPngPageBackground = 2
    _AsPngImagesEmbeddedIntoSvg = 0
    _AsExternalPngFilesReferencedViaSvg = 1
