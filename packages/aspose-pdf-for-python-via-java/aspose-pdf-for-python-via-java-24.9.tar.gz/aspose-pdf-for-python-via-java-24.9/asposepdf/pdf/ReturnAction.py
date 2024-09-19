import jpype 
from asposepdf import Assist 


class ReturnAction(Assist.BaseJavaClass):
    """!Enum represented a program workflow action in case of invoking the
     {@code IWarningCallback.Warning(WarningInfo)} method."""

    java_class_name = "com.aspose.python.pdf.ReturnAction"
    java_class = jpype.JClass(java_class_name)

    Continue = java_class.Continue
    """!
     Used for continue flow.
    
    """

    Abort = java_class.Abort
    """!
     Used for abort flow.
    
    """

