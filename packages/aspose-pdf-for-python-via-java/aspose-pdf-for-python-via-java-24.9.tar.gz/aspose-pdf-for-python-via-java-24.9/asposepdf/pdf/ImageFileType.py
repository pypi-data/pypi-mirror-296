import jpype 
from asposepdf import Assist 


class ImageFileType(Assist.BaseJavaClass):
    """!Enumerates the image file types."""

    java_class_name = "com.aspose.python.pdf.ImageFileType"
    java_class = jpype.JClass(java_class_name)

    Unknown = java_class.Unknown
    """!
     Unknown type.
    
    """

    Svg = java_class.Svg
    """!
     svg image file type.
    
    """

    Dicom = java_class.Dicom
    """!
     Dicom image file type.
    
    """

    Base64 = java_class.Base64
    """!
     Base64 image file type.
    
    """

