import jpype 
from asposepdf import Assist 


class IconCaptionPosition(Assist.BaseJavaClass):
    """!Describes position of icon."""

    java_class_name = "com.aspose.python.pdf.IconCaptionPosition"
    java_class = jpype.JClass(java_class_name)

    NoIcon = java_class.NoIcon
    """!
     Icon is not displayed.
    
    """

    NoCaption = java_class.NoCaption
    """!
     Caption is not displayed.
    
    """

    CaptionBelowIcon = java_class.CaptionBelowIcon
    """!
     Caption is below icon.
    
    """

    CaptionAboveIcon = java_class.CaptionAboveIcon
    """!
     Caption is above icon.
    
    """

    CaptionToTheRight = java_class.CaptionToTheRight
    """!
     Caption to the right.
    
    """

    CaptionToTheLeft = java_class.CaptionToTheLeft
    """!
     Caption to the left.
    
    """

    CaptionOverlaid = java_class.CaptionOverlaid
    """!
     Caption over laid.
    
    """

