import jpype 
from asposepdf import Assist 


class BoxStyle(Assist.BaseJavaClass):
    """!Represents styles of check box"""

    java_class_name = "com.aspose.python.pdf.BoxStyle"
    java_class = jpype.JClass(java_class_name)

    Circle = java_class.Circle
    """!
     Circle style.
    
    """

    Check = java_class.Check
    """!
     Check style.
    
    """

    Cross = java_class.Cross
    """!
     Cross style.
    
    """

    Diamond = java_class.Diamond
    """!
     Diamond style.
    
    """

    Square = java_class.Square
    """!
     Square style.
    
    """

    Star = java_class.Star
    """!
     Star style.
    
    """

