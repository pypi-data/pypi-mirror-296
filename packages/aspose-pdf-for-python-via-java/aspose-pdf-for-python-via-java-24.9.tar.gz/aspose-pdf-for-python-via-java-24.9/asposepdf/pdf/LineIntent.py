import jpype 
from asposepdf import Assist 


class LineIntent(Assist.BaseJavaClass):
    """!Enumerates the intents of the line annotation."""

    java_class_name = "com.aspose.python.pdf.LineIntent"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Undefined state.
    
    """

    LineArrow = java_class.LineArrow
    """!
     Means that the annotation is intended to function as an arrow.
    
    """

    LineDimension = java_class.LineDimension
    """!
     Means that the annotation is intended to function as a dimension line.
    
    """

