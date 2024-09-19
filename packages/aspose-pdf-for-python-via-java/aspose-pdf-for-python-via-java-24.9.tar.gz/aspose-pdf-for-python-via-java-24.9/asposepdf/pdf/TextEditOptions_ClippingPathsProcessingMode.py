import jpype 
from asposepdf import Assist 


class TextEditOptions_ClippingPathsProcessingMode(Assist.BaseJavaClass):
    """!Clipping path processing modes"""

    java_class_name = "com.aspose.python.pdf.TextEditOptions.ClippingPathsProcessingMode"
    java_class = jpype.JClass(java_class_name)

    KeepIntact = java_class.KeepIntact
    """!
     Keeps clipping paths of the original page layout. (Default)
    
    """

    Expand = java_class.Expand
    """!
     Original clipping path will be expanded in the case edited text requires more space.
    
    """

    Remove = java_class.Remove
    """!
     Original clipping path will be removed in the case edited text requires more space. Caution: Because of clipping paths may interact with each other removing of it may lead to unexpected result on the page layout.
    
    """

