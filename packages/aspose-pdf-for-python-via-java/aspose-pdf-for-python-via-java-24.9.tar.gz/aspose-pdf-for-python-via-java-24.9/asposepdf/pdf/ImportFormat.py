import jpype 
from asposepdf import Assist 


class ImportFormat(Assist.BaseJavaClass):
    """!Specifies import format."""

    java_class_name = "com.aspose.python.pdf.ImportFormat"
    java_class = jpype.JClass(java_class_name)

    Cgm = java_class.Cgm
    """!
     Computer Graphics Metafile format.
    
    """

