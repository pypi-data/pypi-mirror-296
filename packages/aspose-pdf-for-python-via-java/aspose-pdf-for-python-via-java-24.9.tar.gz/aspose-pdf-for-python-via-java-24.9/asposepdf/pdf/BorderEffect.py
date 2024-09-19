import jpype 
from asposepdf import Assist 


class BorderEffect(Assist.BaseJavaClass):
    """!Describes effect which should be applied to the border of the annotations."""

    java_class_name = "com.aspose.python.pdf.BorderEffect"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No effect.
    
    """

    Cloudy = java_class.Cloudy
    """!
     The border will appear "cloudly".
    
    """

