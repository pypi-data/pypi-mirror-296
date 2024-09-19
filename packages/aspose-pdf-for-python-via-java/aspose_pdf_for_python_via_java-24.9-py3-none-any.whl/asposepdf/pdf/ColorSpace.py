import jpype 
from asposepdf import Assist 


class ColorSpace(Assist.BaseJavaClass):
    """!The color spaces enumeration."""

    java_class_name = "com.aspose.python.pdf.ColorSpace"
    java_class = jpype.JClass(java_class_name)

    DeviceRGB = java_class.DeviceRGB
    """!
     The device-dependent RGB color space.
    
    """

    DeviceCMYK = java_class.DeviceCMYK
    """!
     The device-dependent CMYK color space.
    
    """

    DeviceGray = java_class.DeviceGray
    """!
     The device-dependent gray color space.
    
    """

