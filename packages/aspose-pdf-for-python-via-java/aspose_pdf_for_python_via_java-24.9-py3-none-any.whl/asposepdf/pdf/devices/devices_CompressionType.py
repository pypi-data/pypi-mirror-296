import jpype 
from asposepdf import Assist 


class devices_CompressionType(Assist.BaseJavaClass):
    """!Used to specify the parameter value passed to a Tiff image device."""

    java_class_name = "com.aspose.python.pdf.devices.CompressionType"
    java_class = jpype.JClass(java_class_name)

    LZW = java_class.LZW
    """!
     Specifies the LZW compression scheme. Can be passed to the Tiff encoder as a parameter that
     belongs to the Compression category.
    
    """

    CCITT4 = java_class.CCITT4
    """!
     Specifies the CCITT4 compression scheme. Can be passed to the CCITT4 encoder as a parameter
     that belongs to the Compression category.
    
    """

    CCITT3 = java_class.CCITT3
    """!
     Specifies the CCITT3 compression scheme. Can be passed to the CCITT3 encoder as a parameter
     that belongs to the Compression category.
    
    """

    RLE = java_class.RLE
    """!
     Specifies the RLE compression scheme. Can be passed to the RLE encoder as a parameter that
     belongs to the Compression category.
    
    """

    Nothing = 4 #get element java_class.getByValue(4) None is reserved word in python - replaced to Nothing
    """!
     Specifies no compression. Can be passed to the Tiff encoder as a parameter that belongs to
     the compression category.
    
    """

