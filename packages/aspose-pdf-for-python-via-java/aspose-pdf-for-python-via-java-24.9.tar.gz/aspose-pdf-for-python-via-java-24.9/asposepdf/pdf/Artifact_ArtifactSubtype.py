import jpype 
from asposepdf import Assist 


class Artifact_ArtifactSubtype(Assist.BaseJavaClass):
    """!Enumeration of possible artifacts subtype."""

    java_class_name = "com.aspose.python.pdf.Artifact.ArtifactSubtype"
    java_class = jpype.JClass(java_class_name)

    Header = java_class.Header
    """!
     Header artifact.
    
    """

    Footer = java_class.Footer
    """!
     Footer artifact.
    
    """

    Watermark = java_class.Watermark
    """!
     Watermark artifact.
    
    """

    Background = java_class.Background
    """!
     Background artifact.
    
    """

    Undefined = java_class.Undefined
    """!
     Artifact subtype is not defined or unknown.
    
    """

