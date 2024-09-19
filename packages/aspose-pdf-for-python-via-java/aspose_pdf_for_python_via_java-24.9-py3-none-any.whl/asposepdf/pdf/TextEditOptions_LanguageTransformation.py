import jpype 
from asposepdf import Assist 


class TextEditOptions_LanguageTransformation(Assist.BaseJavaClass):
    """!Language transformation modes"""

    java_class_name = "com.aspose.python.pdf.TextEditOptions.LanguageTransformation"
    java_class = jpype.JClass(java_class_name)

    Default = java_class.Default
    """!
     Default language transformation is performed.
    
    """

    ExactlyAsISee = java_class.ExactlyAsISee
    """!
     Language transformation is performed the same way as in a text editor. It usually means
     text will looks in the document exactly as You see it in code. But no warranties.
    
    """

    Nothing = 3 #get element java_class.getByValue(3) None is reserved word in python - replaced to Nothing
    """!
     Language transformation is not performed.
    
    """

