import jpype 
from asposepdf import Assist 


class ReplyType(Assist.BaseJavaClass):
    """!Enumerates the kinds of the relationships (the "reply type") between the annotation and one
     specified by InReplyTo."""

    java_class_name = "com.aspose.python.pdf.ReplyType"
    java_class = jpype.JClass(java_class_name)

    Undefined = java_class.Undefined
    """!
     Undefined relationship.
    
    """

    Reply = java_class.Reply
    """!
     The annotation is considered a reply to the annotation specified by InReplyTo. Viewer
     applications should not display replies to an annotation individually but together in the
     form of threaded comments.
    
    """

    Group = java_class.Group
    """!
     The annotation is grouped with the annotation specified by InReplyTo.
    
    """

