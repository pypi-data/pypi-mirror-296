import jpype 
from asposepdf import Assist 


class TextEditOptions_NoCharacterAction(Assist.BaseJavaClass):
    """!Action to perform if font does not contain required character"""

    java_class_name = "com.aspose.python.pdf.TextEditOptions.NoCharacterAction"
    java_class = jpype.JClass(java_class_name)

    ThrowException = java_class.ThrowException
    """!
     Throw exception
    
    """

    UseStandardFont = java_class.UseStandardFont
    """!
     Repalce font to standard font which contains required character
    
    """

    ReplaceAnyway = java_class.ReplaceAnyway
    """!
     Replace text anyway without font substitution
    
    """

    UseCustomReplacementFont = java_class.UseCustomReplacementFont
    """!
     Replace font to defined replacement font
    
    """

