import jpype 
from asposepdf import Assist 


class devices_ColorDepth(Assist.BaseJavaClass):
    """!Used to specify the parameter value passed to a Tiff image device."""

    java_class_name = "com.aspose.python.pdf.devices.ColorDepth"
    java_class = jpype.JClass(java_class_name)

    Default = java_class.Default
    """!
     Default color depth
    
    """

    Format24bpp = java_class.Format24bpp
    """!
     Rgb 24 bit depth.
    
    """

    Format8bpp = java_class.Format8bpp
    """!
     8 bits per pixel. Equal {@code PixelFormat.Format8bppIndexed}
    
    """

    Format4bpp = java_class.Format4bpp
    """!
     4 bits per pixel. Equal {@code PixelFormat.Format4bppIndexed}
    
    """

    Format1bpp = java_class.Format1bpp
    """!
     1 bit per pixel. Equal {@code PixelFormat.Format32bppRgb}
    
    """

