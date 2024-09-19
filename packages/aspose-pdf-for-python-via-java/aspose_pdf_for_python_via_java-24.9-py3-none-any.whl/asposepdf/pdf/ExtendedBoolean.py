import jpype 
from asposepdf import Assist 


class ExtendedBoolean(Assist.BaseJavaClass):
    """!Represents boolean type that supports Undefined value."""

    java_class_name = "com.aspose.python.pdf.ExtendedBoolean"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Undefined value value of ExtendnedBoolean.
    
    """

    False = java_class.False
    """!
     False value of ExtendnedBoolean.
    
    """

    True = java_class.True
    """!
     True value of ExtendnedBoolean.
    
    """

