import jpype 
from asposepdf import Assist 


class ColumnAdjustment(Assist.BaseJavaClass):
    """!Enumerates column adjustment types."""

    java_class_name = "com.aspose.python.pdf.ColumnAdjustment"
    java_class = jpype.JClass(java_class_name)

    Customized = java_class.Customized
    """!
     Customized.
    
    """

    AutoFitToContent = java_class.AutoFitToContent
    """!
     Auto fit to content.
    
    """

    AutoFitToWindow = java_class.AutoFitToWindow
    """!
     Auto fit to window.
    
    """

