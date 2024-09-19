import jpype 
from asposepdf import Assist 


class LightingSchemeType(Assist.BaseJavaClass):
    """!Enum LightingSchemeType: set of lighting scheme types."""

    java_class_name = "com.aspose.python.pdf.LightingSchemeType"
    java_class = jpype.JClass(java_class_name)

    Artwork = java_class.Artwork
    """!
     The "Artwork" lighting scheme.
    
    """

    Nothing = 1 #get element java_class.getByValue(1) None is reserved word in python - replaced to Nothing
    """!
     The "None" lighting scheme.
    
    """

    White = java_class.White
    """!
     The "White" lighting scheme.
    
    """

    Day = java_class.Day
    """!
     The "Day" lighting scheme.
    
    """

    Night = java_class.Night
    """!
     The "Night" lighting scheme.
    
    """

    Hard = java_class.Hard
    """!
     The "Hard" lighting scheme.
    
    """

    Primary = java_class.Primary
    """!
     The "Primary" lighting scheme.
    
    """

    Blue = java_class.Blue
    """!
     The "Blue" lighting scheme.
    
    """

    Red = java_class.Red
    """!
     The "Red" lighting scheme.
    
    """

    Cube = java_class.Cube
    """!
     The "Cube" lighting scheme.
    
    """

    CAD = java_class.CAD
    """!
     The "Cad" lighting scheme.
    
    """

    Headlamp = java_class.Headlamp
    """!
     The "Headlamp" lighting scheme.
    
    """

