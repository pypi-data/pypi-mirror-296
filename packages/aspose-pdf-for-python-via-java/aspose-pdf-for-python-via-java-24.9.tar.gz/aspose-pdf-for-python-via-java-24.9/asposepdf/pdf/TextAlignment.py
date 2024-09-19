import jpype 
from asposepdf import Assist 


class TextAlignment(Assist.BaseJavaClass):
    """!Alignment of text in annotation."""

    java_class_name = "com.aspose.python.pdf.TextAlignment"
    java_class = jpype.JClass(java_class_name)

    Left = java_class.Left
    """!
     Text is aligned to left.
    
    """

    Center = java_class.Center
    """!
     Text is centered.
    
    """

    Right = java_class.Right
    """!
     Text is aligned to right.
    
    """

