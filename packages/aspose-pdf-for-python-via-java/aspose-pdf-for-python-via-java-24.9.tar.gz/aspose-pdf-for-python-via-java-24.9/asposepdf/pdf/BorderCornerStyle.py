import jpype 
from asposepdf import Assist 


class BorderCornerStyle(Assist.BaseJavaClass):
    """!Enumerates the border corner styles for border."""

    java_class_name = "com.aspose.python.pdf.BorderCornerStyle"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     None border style.
    
    """

    Round = java_class.Round
    """!
     Round border style.
    
    """

