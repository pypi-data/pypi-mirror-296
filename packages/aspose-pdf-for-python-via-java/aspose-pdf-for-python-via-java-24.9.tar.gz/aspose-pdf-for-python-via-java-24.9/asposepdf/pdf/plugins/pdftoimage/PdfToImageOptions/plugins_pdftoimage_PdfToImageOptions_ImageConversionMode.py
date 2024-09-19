import jpype 
from asposepdf import Assist 


class plugins_pdftoimage_PdfToImageOptions_ImageConversionMode(Assist.BaseJavaClass):
    """!Defines different modes which can be used while converting from PDF document to Jpeg image. See {@link JpegOptions} class."""

    java_class_name = "com.aspose.python.pdf.plugins.pdftoimage.PdfToImageOptions.ImageConversionMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _None = 0
