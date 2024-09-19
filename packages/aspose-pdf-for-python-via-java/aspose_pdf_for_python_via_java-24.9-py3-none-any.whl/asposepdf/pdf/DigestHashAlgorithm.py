import jpype 
from asposepdf import Assist 


class DigestHashAlgorithm(Assist.BaseJavaClass):
    """!Represent type of algorithm that maps data to a "hash""""

    java_class_name = "com.aspose.python.pdf.DigestHashAlgorithm"
    java_class = jpype.JClass(java_class_name)

    Sha1 = java_class.Sha1
    """!
     SHA-1. Secure Hash Algorithm 1
    
    """

    Sha256 = java_class.Sha256
    """!
     SHA-256. Secure Hash Algorithm 2
    
    """

    Sha512 = java_class.Sha512
    """!
     SHA-512. Secure Hash Algorithm 2
    
    """

