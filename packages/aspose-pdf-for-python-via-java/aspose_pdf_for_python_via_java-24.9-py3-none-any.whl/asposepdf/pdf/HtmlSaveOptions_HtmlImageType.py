import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_HtmlImageType(Assist.BaseJavaClass):
    """!enumerates possible types of image files that can be saved as external resources during Pdf
     to Html conversion"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.HtmlImageType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Tiff = 4
    _Bmp = 2
    _Unknown = 7
    _Gif = 3
    _Svg = 5
    _ZippedSvg = 6
    _Png = 1
    _Jpeg = 0
