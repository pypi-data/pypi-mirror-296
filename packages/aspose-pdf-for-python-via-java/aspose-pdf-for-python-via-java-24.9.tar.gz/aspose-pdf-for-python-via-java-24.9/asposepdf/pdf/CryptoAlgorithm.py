import jpype 
from asposepdf import Assist 


class CryptoAlgorithm(Assist.BaseJavaClass):
    """!Represent type of cryptographic algorithm that used in encryption/decryption routines."""

    java_class_name = "com.aspose.python.pdf.CryptoAlgorithm"
    java_class = jpype.JClass(java_class_name)

    RC4x40 = java_class.RC4x40
    """!
     RC4 with key length 40.
    
    """

    RC4x128 = java_class.RC4x128
    """!
     RC4 with key length 128.
    
    """

    AESx128 = java_class.AESx128
    """!
     AES with key length 128.
    
    """

    AESx256 = java_class.AESx256
    """!
     AES with key length 256.
    
    """


