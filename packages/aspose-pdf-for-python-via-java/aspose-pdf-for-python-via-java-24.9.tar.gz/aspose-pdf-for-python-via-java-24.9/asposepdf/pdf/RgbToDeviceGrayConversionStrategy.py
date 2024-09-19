import jpype 
from asposepdf import Assist 


class RgbToDeviceGrayConversionStrategy(Assist.BaseJavaClass):
    """!Represents rgb to device gray color spaces conversion strategy."""

    java_class_name = "com.aspose.python.pdf.RgbToDeviceGrayConversionStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
