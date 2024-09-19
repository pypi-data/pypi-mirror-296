import jpype 
from asposepdf import Assist 


class CaretSymbol(Assist.BaseJavaClass):
    """!A symbol to be associated with the caret."""

    java_class_name = "com.aspose.python.pdf.CaretSymbol"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No symbol should be associated with the caret.
    
    """

    Paragraph = java_class.Paragraph
    """!
     A new paragraph symbol should be associated with the caret.
    
    """

