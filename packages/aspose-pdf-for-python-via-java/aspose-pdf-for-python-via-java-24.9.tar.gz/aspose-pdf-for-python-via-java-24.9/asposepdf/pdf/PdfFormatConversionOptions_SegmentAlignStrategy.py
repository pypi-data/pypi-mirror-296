import jpype 
from asposepdf import Assist 


class PdfFormatConversionOptions_SegmentAlignStrategy(Assist.BaseJavaClass):
    """!Describes strategies used to align document text segments. Now only strategy to restore
     segments to original bounds is supported. In future another strategies could be added."""

    java_class_name = "com.aspose.python.pdf.PdfFormatConversionOptions.SegmentAlignStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _None = 0
    _RestoreSegmentBounds = 1
