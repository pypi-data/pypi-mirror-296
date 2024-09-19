import jpype 
from asposepdf import Assist 


class ColorType(Assist.BaseJavaClass):
    """!Specifies color type of elements on page."""

    java_class_name = "com.aspose.python.pdf.ColorType"
    java_class = jpype.JClass(java_class_name)

    Rgb = java_class.Rgb
    """!
     RGB color type.
    
    """

    Grayscale = java_class.Grayscale
    """!
     Grayscale color type.
    
    """

    BlackAndWhite = java_class.BlackAndWhite
    """!
     Black and white color type.
    
    """

    Undefined = java_class.Undefined
    """!
     Undefined color type value.
    
    """

