import jpype 
from asposepdf import Assist 


class AnnotationState(Assist.BaseJavaClass):
    """!The enumeration of states to which the original annotation can be set."""

    java_class_name = "com.aspose.python.pdf.AnnotationState"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Not defined state.
    
    """

    Marked = java_class.Marked
    """!
     The annotation has been marked by the user.
    
    """

    Unmarked = java_class.Unmarked
    """!
     The annotation has not been marked by the user.
    
    """

    Accepted = java_class.Accepted
    """!
     The user agrees with the change.
    
    """

    Rejected = java_class.Rejected
    """!
     The user disagrees with the change.
    
    """

    Cancelled = java_class.Cancelled
    """!
     The change has been cancelled.
    
    """

    Completed = java_class.Completed
    """!
     The change has been completed.
    
    """

    Nothing = 7 #get element java_class.getByValue(7) None is reserved word in python - replaced to Nothing
    """!
     The user has indicated nothing about the change.
    
    """

