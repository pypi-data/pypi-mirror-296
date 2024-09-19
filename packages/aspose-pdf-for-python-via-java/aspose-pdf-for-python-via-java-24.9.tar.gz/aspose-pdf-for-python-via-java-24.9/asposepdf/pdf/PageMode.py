import jpype 
from asposepdf import Assist 


class PageMode(Assist.BaseJavaClass):
    """!Class descibes used components of the document page."""

    java_class_name = "com.aspose.python.pdf.PageMode"
    java_class = jpype.JClass(java_class_name)

    UseNone = java_class.UseNone
    """!
     Dont use any components.
    
    """

    UseOutlines = java_class.UseOutlines
    """!
     Document outline visible.
    
    """

    UseThumbs = java_class.UseThumbs
    """!
     Thumbnail images visible.
    
    """

    FullScreen = java_class.FullScreen
    """!
     FullScreenFull-screen mode, with no menu bar, window controls, or any other window visible.
    
    """

    UseOC = java_class.UseOC
    """!
    """

    UseAttachments = java_class.UseAttachments
    """!
     Attachments panel visible.
    
    """

