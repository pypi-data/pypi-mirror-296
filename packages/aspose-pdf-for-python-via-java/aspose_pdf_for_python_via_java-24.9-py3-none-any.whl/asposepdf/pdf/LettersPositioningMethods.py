import jpype 
from asposepdf import Assist 


class LettersPositioningMethods(Assist.BaseJavaClass):
    """!It enumerates possible modes of positioning of letters in words in result HTML"""

    java_class_name = "com.aspose.python.pdf.LettersPositioningMethods"
    java_class = jpype.JClass(java_class_name)

    UseEmUnitsAndCompensationOfRoundingErrorsInCss = java_class.UseEmUnitsAndCompensationOfRoundingErrorsInCss
    """!
     It's default method. It uses EM-units and special algorithm of compensation of rounding
     errors It's preferable for usage in IE10.0 and more fresh versions and gives better scaling
     of captions when scaling is necessary
    
    """

    UsePixelUnitsInCssLetterSpacingForIE = java_class.UsePixelUnitsInCssLetterSpacingForIE
    """!
     It allows to get sometimes more precise results in old IE browser versions
    
    """

