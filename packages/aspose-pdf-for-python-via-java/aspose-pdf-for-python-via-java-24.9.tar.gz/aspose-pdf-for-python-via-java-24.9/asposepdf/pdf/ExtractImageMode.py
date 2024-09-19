import jpype 
from asposepdf import Assist 


class ExtractImageMode(Assist.BaseJavaClass):
    """!Defines different modes which can be used while extracting images from documents."""

    java_class_name = "com.aspose.python.pdf.ExtractImageMode"
    java_class = jpype.JClass(java_class_name)

    DefinedInResources = java_class.DefinedInResources
    """!
     Defines image extraction mode in which all images defined in resources for particular page
     are extracted.
    
    """

    ActuallyUsed = java_class.ActuallyUsed
    """!
     Defines image extraction mode in which only those images are extracted that are actually
     shown on a page.
    
    """

