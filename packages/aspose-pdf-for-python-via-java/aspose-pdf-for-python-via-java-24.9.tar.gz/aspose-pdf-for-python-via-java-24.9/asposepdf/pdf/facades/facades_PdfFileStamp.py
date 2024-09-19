import jpype 
from asposepdf import Assist 


class facades_PdfFileStamp(Assist.BaseJavaClass):
    """!Class for adding stamps (watermark or background) to PDF files."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileStamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _POS_BOTTOM_LEFT = 5
    _POS_SIDES_LEFT = 6
    _POS_BOTTOM_MIDDLE = 0
    _POS_UPPER_RIGHT = 2
    _POS_SIDES_RIGHT = 3
    _POS_UPPER_MIDDLE = 4
    _POS_BOTTOM_RIGHT = 1
    _POS_UPPER_LEFT = 7
