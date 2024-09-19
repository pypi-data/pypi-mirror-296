import jpype 
from asposepdf import Assist 


class CaptionPosition(Assist.BaseJavaClass):
    """!Enumeration of the annotation's caption positioning."""

    java_class_name = "com.aspose.python.pdf.CaptionPosition"
    java_class = jpype.JClass(java_class_name)

    Inline = java_class.Inline
    """!
     The caption will be centered inside the line (default value).
    
    """

    Top = java_class.Top
    """!
     The caption will be on top of the line.
    
    """

