import jpype 
from asposepdf import Assist 


class HtmlMediaType(Assist.BaseJavaClass):
    """!Specifies possible media types used during rendering."""

    java_class_name = "com.aspose.python.pdf.HtmlMediaType"
    java_class = jpype.JClass(java_class_name)

    Print = java_class.Print
    """!
     Print.
    
    """

    Screen = java_class.Screen
    """!
     Screen.
    
    """

