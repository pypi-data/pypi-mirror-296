import jpype 
from asposepdf import Assist 


class ColorsOfCMYK(Assist.BaseJavaClass):
    """!Colors included in the CMYK color model."""

    java_class_name = "com.aspose.python.pdf.ColorsOfCMYK"
    java_class = jpype.JClass(java_class_name)

    Cyan = java_class.Cyan
    """!
     Cyan color.
    
    """

    Magenta = java_class.Magenta
    """!
     Magenta color.
    
    """

    Yellow = java_class.Yellow
    """!
     Yellow color.
    
    """

    Black = java_class.Black
    """!
     Black color.
    
    """

