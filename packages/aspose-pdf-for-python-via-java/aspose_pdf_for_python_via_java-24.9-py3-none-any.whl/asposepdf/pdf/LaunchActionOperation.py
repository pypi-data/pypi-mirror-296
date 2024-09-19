import jpype 
from asposepdf import Assist 


class LaunchActionOperation(Assist.BaseJavaClass):
    """!Enumerates the operations to perform with document during launch action executing."""

    java_class_name = "com.aspose.python.pdf.LaunchActionOperation"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Undefined state.
    
    """

    Open = java_class.Open
    """!
     Open a document.
    
    """

    Print = java_class.Print
    """!
     Print a document.
    
    """

