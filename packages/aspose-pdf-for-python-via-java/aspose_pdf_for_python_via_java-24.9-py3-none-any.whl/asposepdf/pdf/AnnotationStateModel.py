import jpype 
from asposepdf import Assist 


class AnnotationStateModel(Assist.BaseJavaClass):
    """!The state model corresponding to state of annotation."""

    java_class_name = "com.aspose.python.pdf.AnnotationStateModel"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Not defined state model.
    
    """

    Marked = java_class.Marked
    """!
     The annotation has been marked (or unmarked) by the user.
    
    """

    Review = java_class.Review
    """!
     The annotation has been reviewed (accepted, rejected, cancelled, completed, none) by the
     user.
    
    """

