import jpype 
from asposepdf import Assist 


class DocMDPAccessPermissions(Assist.BaseJavaClass):
    """!The access permissions granted for this document. Valid values are: 1 - No changes to the
     document are permitted; any change to the document invalidates the signature. 2 - Permitted
     changes are filling in forms, instantiating page templates, and signing; other changes invalidate
     the signature. 3 - Permitted changes are the same as for 2, as well as annotation creation,
     deletion, and modification; other changes invalidate the signature."""

    java_class_name = "com.aspose.python.pdf.DocMDPAccessPermissions"
    java_class = jpype.JClass(java_class_name)

    NoChanges = java_class.NoChanges
    """!
     1 - No changes to the document are permitted; any change to the document invalidates the
     signature.
    
    """

    FillingInForms = java_class.FillingInForms
    """!
     2 - Permitted changes are filling in forms, instantiating page templates, and signing; other
     changes invalidate the signature.
    
    """

    AnnotationModification = java_class.AnnotationModification
    """!
     3 - Permitted changes are the same as for 2, as well as annotation creation, deletion, and
     modification; other changes invalidate the signature.
    
    """

