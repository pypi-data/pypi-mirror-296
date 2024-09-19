import jpype 
from asposepdf import Assist 


class NumberingStyle(Assist.BaseJavaClass):
    """!Enumeration of supported page numbering style for PageLabel class."""

    java_class_name = "com.aspose.python.pdf.NumberingStyle"
    java_class = jpype.JClass(java_class_name)

    NumeralsArabic = java_class.NumeralsArabic
    """!
     Arabic decimal numbers.
    
    """

    NumeralsRomanUppercase = java_class.NumeralsRomanUppercase
    """!
     Uppercase roman numbers (I, II, III...).
    
    """

    NumeralsRomanLowercase = java_class.NumeralsRomanLowercase
    """!
     Lowercase roman numbers (i, ii, iii...).
    
    """

    LettersUppercase = java_class.LettersUppercase
    """!
     Uppercase latin letters (A, B, C...).
    
    """

    LettersLowercase = java_class.LettersLowercase
    """!
     Lowercase latin letters (a, b, c...).
    
    """

    Nothing = 5 #get element java_class.getByValue(5) None is reserved word in python - replaced to Nothing
    """!
     No numbering.
    
    """

