import jpype 
from asposepdf import Assist 


class SaveOptions_HtmlBorderLineType(Assist.BaseJavaClass):
    """!Represents line types that can be used in result document for drawing borders or another
     lines"""

    java_class_name = "com.aspose.python.pdf.SaveOptions.HtmlBorderLineType"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No line will be shown.
    
    """

    Dotted = java_class.Dotted
    """!
     Dotted line will be shown.
    
    """

    Dashed = java_class.Dashed
    """!
     Dashed line will be shown.
    
    """

    Solid = java_class.Solid
    """!
     Ssolid line will be shown.
    
    """

    Double = java_class.Double
    """!
     Double line will be shown.
    
    """

    Groove = java_class.Groove
    """!
     Groove line will be shown.
    
    """

    Ridge = java_class.Ridge
    """!
     Ridge line will be shown.
    
    """

    Inset = java_class.Inset
    """!
     Inset line will be shown.
    
    """

    Outset = java_class.Outset
    """!
     Outset line will be shown.
    
    """

