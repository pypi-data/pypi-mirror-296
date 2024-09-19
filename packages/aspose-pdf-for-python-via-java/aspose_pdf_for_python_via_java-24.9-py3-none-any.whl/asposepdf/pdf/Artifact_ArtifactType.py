import jpype 
from asposepdf import Assist 


class Artifact_ArtifactType(Assist.BaseJavaClass):
    """!Enumeration of possible artifact types."""

    java_class_name = "com.aspose.python.pdf.Artifact.ArtifactType"
    java_class = jpype.JClass(java_class_name)

    Pagination = java_class.Pagination
    """!
     Pagination artifacts. Ancillary page features such as running heads and folios (page
     numbers).
    
    """

    Layout = java_class.Layout
    """!
     Layout artifacts. Purely cosmetic typographical or design elements such as footnote rules
     or background screens.
    
    """

    Page = java_class.Page
    """!
     Page artifacts. Production aids extraneous to the document itself, such as cut marks and
     colour bars.
    
    """

    Background = java_class.Background
    """!
     Background artifacts. Images, patterns or coloured blocks.
    
    """

    Undefined = java_class.Undefined
    """!
     Artifact type is not defined or unknown.
    
    """

