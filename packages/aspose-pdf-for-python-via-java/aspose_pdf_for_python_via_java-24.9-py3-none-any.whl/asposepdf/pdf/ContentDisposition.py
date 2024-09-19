import jpype 
from asposepdf import Assist 


class ContentDisposition(Assist.BaseJavaClass):
    """!MIME protocol Content-Disposition header."""

    java_class_name = "com.aspose.python.pdf.ContentDisposition"
    java_class = jpype.JClass(java_class_name)

    Inline = java_class.Inline
    """!
     Result is shown inline.
    
    """

    Attachment = java_class.Attachment
    """!
     Result is saved as attachment.
    
    """

