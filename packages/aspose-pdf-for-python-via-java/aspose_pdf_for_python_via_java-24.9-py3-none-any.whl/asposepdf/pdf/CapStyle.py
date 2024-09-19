import jpype 
from asposepdf import Assist 


class CapStyle(Assist.BaseJavaClass):
    """!Style of line ending of Ink annotation line."""

    java_class_name = "com.aspose.python.pdf.CapStyle"
    java_class = jpype.JClass(java_class_name)

    Rectangular = java_class.Rectangular
    """!
     End is rectangular.
    
    """

    Rounded = java_class.Rounded
    """!
     End is rounded.
    
    """

