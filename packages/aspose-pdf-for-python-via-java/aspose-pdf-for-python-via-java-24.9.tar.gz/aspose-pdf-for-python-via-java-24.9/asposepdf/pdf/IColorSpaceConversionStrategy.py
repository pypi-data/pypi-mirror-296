import jpype 
from asposepdf import Assist 


class IColorSpaceConversionStrategy(Assist.BaseJavaClass):
    """!Interface for color space conversion strategies."""

    java_class_name = "com.aspose.python.pdf.IColorSpaceConversionStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
