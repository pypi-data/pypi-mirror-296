import jpype 
from asposepdf import Assist 


class BorderStyle(Assist.BaseJavaClass):
    """!Describes style of the annotation border."""

    java_class_name = "com.aspose.python.pdf.BorderStyle"
    java_class = jpype.JClass(java_class_name)

    Solid = java_class.Solid
    """!
     Solid border.
    
    """

    Dashed = java_class.Dashed
    """!
     Dashed border.
    
    """

    Beveled = java_class.Beveled
    """!
     Bevelled border.
    
    """

    Inset = java_class.Inset
    """!
     Inset border.
    
    """

    Underline = java_class.Underline
    """!
     Underlined border.
    
    """

