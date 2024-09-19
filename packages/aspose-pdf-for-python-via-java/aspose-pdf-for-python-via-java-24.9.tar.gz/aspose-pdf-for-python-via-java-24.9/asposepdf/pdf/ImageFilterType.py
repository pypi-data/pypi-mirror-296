import jpype 
from asposepdf import Assist 


class ImageFilterType(Assist.BaseJavaClass):
    """!Enumeration representing image filter type."""

    java_class_name = "com.aspose.python.pdf.ImageFilterType"
    java_class = jpype.JClass(java_class_name)

    Jpeg2000 = java_class.Jpeg2000
    """!
     Jpeg2000 filter
    
    """

    Jpeg = java_class.Jpeg
    """!
     Jpeg filter
    
    """

    Flate = java_class.Flate
    """!
     Flate filter
    
    """

    CCITTFax = java_class.CCITTFax
    """!
     CCITTFax filter
    
    """

