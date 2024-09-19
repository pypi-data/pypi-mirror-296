import jpype 
from asposepdf import Assist 


class TextReplaceOptions_ReplaceAdjustment(Assist.BaseJavaClass):
    """!Determines action that will be done after replace of text fragment to more short.
     None - no action, replaced text may overlaps rest of the line;
     AdjustSpaceWidth - tries adjust spaces between words to keep line length;
     WholeWordsHyphenation - tries distribute words between paragraph lines to keep paragraph's right field;
     ShiftRestOfLine - shifts rest of the line according to changing length of text, length of the line may be changed;
     Default value is ShiftRestOfLine."""

    java_class_name = "com.aspose.python.pdf.TextReplaceOptions.ReplaceAdjustment"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No action, replaced text may overlaps rest of the line
    
    """

    AdjustSpaceWidth = java_class.AdjustSpaceWidth
    """!
     Tries adjust spaces between words to keep line length
    
    """

    WholeWordsHyphenation = java_class.WholeWordsHyphenation
    """!
     Tries distribute words between paragraph lines to keep paragraph's right field
    
    """

    IsFormFillingMode = java_class.IsFormFillingMode
    """!
     Tries to spread the words in the available white space using the paragraph width.
     If the text overflows, it will be hidden.
    
    """

    ShiftRestOfLine = java_class.ShiftRestOfLine
    """!
     (Default) Shifts rest of the line according to changing length of text, length of the line may be changed
    
    """

