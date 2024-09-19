import jpype 
from asposepdf import Assist 


class PolyIntent(Assist.BaseJavaClass):
    """!Enumerates the intents of the polygon or polyline annotation."""

    java_class_name = "com.aspose.python.pdf.PolyIntent"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Undefined state.
    
    """

    PolygonCloud = java_class.PolygonCloud
    """!
     Means that the annotation is intended to function as a cloud object.
    
    """

    PolyLineDimension = java_class.PolyLineDimension
    """!
     Indicates that the polyline annotation is intended to function as a dimension.
    
    """

    PolygonDimension = java_class.PolygonDimension
    """!
     Indicates that the polygon annotation is intended to function as a dimension.
    
    """

