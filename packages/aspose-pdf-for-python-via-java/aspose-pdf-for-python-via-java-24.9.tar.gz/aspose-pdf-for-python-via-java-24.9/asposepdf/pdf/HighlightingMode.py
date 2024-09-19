import jpype 
from asposepdf import Assist 


class HighlightingMode(Assist.BaseJavaClass):
    """!Enumerates the annotation's highlighting mode, the visual effect to be used when the mouse button
     is pressed or held down inside its active area."""

    java_class_name = "com.aspose.python.pdf.HighlightingMode"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No highlighting.
    
    """

    Invert = java_class.Invert
    """!
     Invert the contents of the annotation rectangle.
    
    """

    Outline = java_class.Outline
    """!
     Invert the annotation's border.
    
    """

    Push = java_class.Push
    """!
     Display the annotation's down appearance, if any. If no down appearance is defined, offset
     the contents of the annotation rectangle to appear as if it were being pushed below the
     surface of the page.
    
    """

    Toggle = java_class.Toggle
    """!
     Same as Push (which is preferred).
    
    """

