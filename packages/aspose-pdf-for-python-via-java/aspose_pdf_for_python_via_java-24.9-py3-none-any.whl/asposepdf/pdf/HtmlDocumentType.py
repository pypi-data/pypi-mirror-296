import jpype 
from asposepdf import Assist 


class HtmlDocumentType(Assist.BaseJavaClass):
    """!Represents enumeration of the Html document types."""

    java_class_name = "com.aspose.python.pdf.HtmlDocumentType"
    java_class = jpype.JClass(java_class_name)

    Xhtml = java_class.Xhtml
    """!
     The XHtml Document Type.
    
    """

    Html5 = java_class.Html5
    """!
     The HTML5 Document Type.
    
    """

