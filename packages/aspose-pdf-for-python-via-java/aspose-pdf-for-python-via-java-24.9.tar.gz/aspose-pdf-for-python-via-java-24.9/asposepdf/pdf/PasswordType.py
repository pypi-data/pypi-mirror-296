import jpype 
from asposepdf import Assist 


class PasswordType(Assist.BaseJavaClass):
    """!This enum represents known password types used for password protected pdf documents."""

    java_class_name = "com.aspose.python.pdf.PasswordType"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     Pdf document is not password protected.
    
    """

    User = java_class.User
    """!
     Pdf document was opened using document open password (restricted access).
    
    """

    Owner = java_class.Owner
    """!
     Pdf document was opened using change permissions password (full access).
    
    """

    Inaccessible = java_class.Inaccessible
    """!
     Pdf document is password protected but both user and owner passwords are not empty and none
     of the passwords was defined or supplied password was incorrect. So it impossible to deduce
     the type of the password.
    
    """

