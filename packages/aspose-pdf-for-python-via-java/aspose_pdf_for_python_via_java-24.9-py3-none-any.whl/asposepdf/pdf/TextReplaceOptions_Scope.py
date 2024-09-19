import jpype 
from asposepdf import Assist 


class TextReplaceOptions_Scope(Assist.BaseJavaClass):
    """!Scope where replace text operation is applied REPLACE_FIRST by default This obsolete option
     was kept for compatibility. It affects to PdfContentEditor and has no effect to
     TextFragmentAbsorber."""

    java_class_name = "com.aspose.python.pdf.TextReplaceOptions.Scope"
    java_class = jpype.JClass(java_class_name)

    REPLACE_FIRST = java_class.REPLACE_FIRST
    """!
     Replace only first occurrence of the text on each of affected pages
    
    """

    REPLACE_ALL = java_class.REPLACE_ALL
    """!
     Replace all text occurrences on all affected pages
    
    """

