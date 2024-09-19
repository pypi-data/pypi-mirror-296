import jpype 
from asposepdf import Assist 


class devices_ShapeType(Assist.BaseJavaClass):
    """!This enum represents shape type for the extracted images."""

    java_class_name = "com.aspose.python.pdf.devices.ShapeType"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     Original image shape.
    
    """

    Landscape = java_class.Landscape
    """!
     Landscape Shape.
    
    """

    Portrait = java_class.Portrait
    """!
     Portrait Shape.
    
    """

