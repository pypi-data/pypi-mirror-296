import jpype 
from asposepdf import Assist 


class Direction(Assist.BaseJavaClass):
    """!Text direction."""

    java_class_name = "com.aspose.python.pdf.Direction"
    java_class = jpype.JClass(java_class_name)

    L2R = java_class.L2R
    """!
     Left to right direction.
    
    """

    R2L = java_class.R2L
    """!
     Right to left direction.
    
    """

