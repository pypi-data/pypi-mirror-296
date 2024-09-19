import jpype 
from asposepdf import Assist 


class LineEnding(Assist.BaseJavaClass):
    """!Enumerates the line ending styles to be used in drawing the line."""

    java_class_name = "com.aspose.python.pdf.LineEnding"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No line ending.
    
    """

    Square = java_class.Square
    """!
     A square filled with the annotation's interior color, if any.
    
    """

    Circle = java_class.Circle
    """!
     A circle filled with the annotation's interior color, if any.
    
    """

    Diamond = java_class.Diamond
    """!
     A diamond shape filled with the annotation's interior color, if any.
    
    """

    OpenArrow = java_class.OpenArrow
    """!
     Two short lines meeting in an acute angle to form an open arrowhead.
    
    """

    ClosedArrow = java_class.ClosedArrow
    """!
     Two short lines meeting in an acute angle as in the OpenArrow style and connected by a third
     line to form a triangular closed arrowhead filled with the annotation's interior color, if
     any.
    
    """

    Butt = java_class.Butt
    """!
     A short line at the endpoint perpendicular to the line itself.
    
    """

    ROpenArrow = java_class.ROpenArrow
    """!
     Two short lines in the reverse direction from OpenArrow.
    
    """

    RClosedArrow = java_class.RClosedArrow
    """!
     A triangular closed arrowhead in the reverse direction from ClosedArrow.
    
    """

    Slash = java_class.Slash
    """!
     A short line at the endpoint approximately 30 degrees clockwise from perpendicular to the
     line itself.
    
    """

