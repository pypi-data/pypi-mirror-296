import jpype 
from asposepdf import Assist 


class AFRelationship(Assist.BaseJavaClass):
    """!Enumeration describes associated files relationship."""

    java_class_name = "com.aspose.python.pdf.AFRelationship"
    java_class = jpype.JClass(java_class_name)

    Source = java_class.Source
    """!
     Source
    
    """

    Data = java_class.Data
    """!
     Data
    
    """

    Alternative = java_class.Alternative
    """!
     Alternative
    
    """

    Supplement = java_class.Supplement
    """!
     Supplement
    
    """

    Unspecified = java_class.Unspecified
    """!
     Unspecified
    
    """

    EncryptedPayload = java_class.EncryptedPayload
    """!
     EncryptedPayload
    
    """

    Nothing = 6 #get element java_class.getByValue(6) None is reserved word in python - replaced to Nothing
    """!
     None
    
    """

