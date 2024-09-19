import jpype 
from asposepdf import Assist 


class OptimizedMemoryStream_SeekOrigin(Assist.BaseJavaClass):
    """!Specifies the position in a stream to use for seeking."""

    java_class_name = "com.aspose.python.pdf.OptimizedMemoryStream.SeekOrigin"
    java_class = jpype.JClass(java_class_name)

    Begin = java_class.Begin
    """!
     Specifies the beginning of a stream.
    
    """

    Current = java_class.Current
    """!
     Specifies the current position within a stream.
    
    """

    End = java_class.End
    """!
     Specifies the end of a stream.
    
    """

