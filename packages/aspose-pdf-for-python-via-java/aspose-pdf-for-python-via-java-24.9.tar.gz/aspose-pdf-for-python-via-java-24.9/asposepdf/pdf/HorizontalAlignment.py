import jpype 
from asposepdf import Assist 


class HorizontalAlignment(Assist.BaseJavaClass):
    """!Describes horizontal alignment."""

    java_class_name = "com.aspose.python.pdf.HorizontalAlignment"
    java_class = jpype.JClass(java_class_name)

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
     No alignment.
    
    """

    Left = java_class.Left
    """!
     Align to left.
    
    """

    Center = java_class.Center
    """!
     Center alignment.
    
    """

    Right = java_class.Right
    """!
     Align to right.
    
    """

    Justify = java_class.Justify
    """!
     Justify alignment. Text will be aligned on both left and right margins.
    
    """

    FullJustify = java_class.FullJustify
    """!
     Similar to 'Justify' alignment, except that the very last line will only be left-aligned in
     'Justify' mode, while in 'FullJustify' mode all lines will be left- and right-aligned.
    
    """

