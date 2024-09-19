import jpype 
from asposepdf import Assist 


class facades_ImageMergeMode(Assist.BaseJavaClass):
    """!Represents modes for merging images."""

    java_class_name = "com.aspose.python.pdf.facades.ImageMergeMode"
    java_class = jpype.JClass(java_class_name)

    Vertical = java_class.Vertical
    """!
     Images merged vertically.
    
    """

    Horizontal = java_class.Horizontal
    """!
     Images merged horizontally.
    
    """

    Center = java_class.Center
    """!
     Images aligned by center.
    
    """

