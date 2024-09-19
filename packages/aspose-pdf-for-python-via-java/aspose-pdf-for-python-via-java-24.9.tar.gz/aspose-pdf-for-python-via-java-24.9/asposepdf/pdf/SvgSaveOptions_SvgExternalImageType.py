import jpype 
from asposepdf import Assist 


class SvgSaveOptions_SvgExternalImageType(Assist.BaseJavaClass):
    """!enumerates possible types of image files that can be saved as external resources during
     during Pdf to SVG conversion"""

    java_class_name = "com.aspose.python.pdf.SvgSaveOptions.SvgExternalImageType"
    java_class = jpype.JClass(java_class_name)

    Jpeg = java_class.Jpeg
    """!
     Jpeg format
    
    """

    Png = java_class.Png
    """!
     Png format
    
    """

    Bmp = java_class.Bmp
    """!
     Bmp format
    
    """

    Gif = java_class.Gif
    """!
     Gif format
    
    """

    Tiff = java_class.Tiff
    """!
     Tiff format
    
    """

    Unknown = java_class.Unknown
    """!
     Unknown - means that converter cannot detect type of content itself
    
    """

