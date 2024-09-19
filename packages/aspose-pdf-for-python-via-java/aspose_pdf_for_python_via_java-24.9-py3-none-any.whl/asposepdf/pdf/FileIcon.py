import jpype 
from asposepdf import Assist 


class FileIcon(Assist.BaseJavaClass):
    """!An icon to be used in displaying the annotation."""

    java_class_name = "com.aspose.python.pdf.FileIcon"
    java_class = jpype.JClass(java_class_name)

    PushPin = java_class.PushPin
    """!
     PushPin icon (default value).
    
    """

    Graph = java_class.Graph
    """!
     Graph icon.
    
    """

    Paperclip = java_class.Paperclip
    """!
     Paperclip icon.
    
    """

    Tag = java_class.Tag
    """!
     This is tag icon.
    
    """

