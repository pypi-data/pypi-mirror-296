import jpype 
from asposepdf import Assist 


class FileEncoding(Assist.BaseJavaClass):
    """!Encoding of the attached file. Possible values: Zip - file is compressed with ZIP, None - file is
     non compressed."""

    java_class_name = "com.aspose.python.pdf.FileEncoding"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     File is not compressed.
    
    """

    Zip = java_class.Zip
    """!
     File is compressed with ZIP algorithhm.
    
    """

