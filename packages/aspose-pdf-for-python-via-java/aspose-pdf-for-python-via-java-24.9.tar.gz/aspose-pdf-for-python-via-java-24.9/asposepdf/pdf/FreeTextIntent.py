import jpype 
from asposepdf import Assist 


class FreeTextIntent(Assist.BaseJavaClass):
    """!Enumerates the intents of the free text annotation."""

    java_class_name = "com.aspose.python.pdf.FreeTextIntent"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Not defined state.
    
    """

    FreeTextCallout = java_class.FreeTextCallout
    """!
     Means that the annotation is intended to function as a callout.
    
    """

    FreeTextTypeWriter = java_class.FreeTextTypeWriter
    """!
     Means that the annotation is intended to function as a click-to-type or typewriter object.
    
    """

