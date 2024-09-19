import jpype 
from asposepdf import Assist 


class Justification(Assist.BaseJavaClass):
    """!Enumerates the forms of quadding (justification) to be used in displaying the annotation's text."""

    java_class_name = "com.aspose.python.pdf.Justification"
    java_class = jpype.JClass(java_class_name)

    Left = java_class.Left
    """!
     Left justification.
    
    """

    Center = java_class.Center
    """!
     Center justification.
    
    """

    Right = java_class.Right
    """!
     Right justification.
    
    """

