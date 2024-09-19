import jpype 
from asposepdf import Assist 


class ImageFormat(Assist.BaseJavaClass):
    """!This enum represents image formats."""

    java_class_name = "com.aspose.python.pdf.ImageFormat"
    java_class = jpype.JClass(java_class_name)

    Bmp = java_class.Bmp
    """!
     BMP format.
    
    """

    Jpeg = java_class.Jpeg
    """!
     JPEG format.
    
    """

    Gif = java_class.Gif
    """!
     GIF format.
    
    """

    Png = java_class.Png
    """!
     PNG format.
    
    """

    Tiff = java_class.Tiff
    """!
     TIFF format.
    
    """

    Emf = java_class.Emf
    """!
     EMF format.
    
    """

    Dicom = java_class.Dicom
    """!
     DICOM format.
    
    """

    MemoryBmp = java_class.MemoryBmp
    """!
     MemoryBmp format.
    
    """

    Wmf = java_class.Wmf
    """!
     Wmf format.
    
    """

    Exif = java_class.Exif
    """!
     Exif format.
    
    """

