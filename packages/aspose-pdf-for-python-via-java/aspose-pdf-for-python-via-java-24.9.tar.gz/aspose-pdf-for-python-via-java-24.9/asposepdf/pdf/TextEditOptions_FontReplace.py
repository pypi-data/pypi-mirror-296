import jpype 
from asposepdf import Assist 


class TextEditOptions_FontReplace(Assist.BaseJavaClass):
    """!Font replacement behavior."""

    java_class_name = "com.aspose.python.pdf.TextEditOptions.FontReplace"
    java_class = jpype.JClass(java_class_name)

    Default = java_class.Default
    """!
     No additional changes performed during font replacement.
    
    """

    RemoveUnusedFonts = java_class.RemoveUnusedFonts
    """!
     Fonts that become unused during font replacement will be removed from resulting document.
    
    """

