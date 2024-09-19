import jpype 
from asposepdf import Assist 


class Fixup(Assist.BaseJavaClass):
    """!This enum represents an type of Fixup."""

    java_class_name = "com.aspose.python.pdf.Fixup"
    java_class = jpype.JClass(java_class_name)

    ConvertAllPagesIntoCMYKImagesAndPreserveTextInformation = java_class.ConvertAllPagesIntoCMYKImagesAndPreserveTextInformation
    """!
     Not supported.
    
    """

    ConvertFontsToOutlines = java_class.ConvertFontsToOutlines
    """!
     Not supported.
    
    """

    DerivePageGeometryBoxesFromCropMarks = java_class.DerivePageGeometryBoxesFromCropMarks
    """!
     Not supported.
    
    """

    EmbedMissingFonts = java_class.EmbedMissingFonts
    """!
     Not supported.
    
    """

    RotatePagesToLandscape = java_class.RotatePagesToLandscape
    """!
     Rotate all pages to landscape if portrait by 90 degrees.
    
    """

    RotatePagesToPortrait = java_class.RotatePagesToPortrait
    """!
     Rotate all pages to portrait if landscape by 90 degrees.
    
    """

