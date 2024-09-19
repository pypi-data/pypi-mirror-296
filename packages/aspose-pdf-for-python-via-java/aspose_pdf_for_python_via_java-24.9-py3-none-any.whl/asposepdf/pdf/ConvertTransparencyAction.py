import jpype 
from asposepdf import Assist 


class ConvertTransparencyAction(Assist.BaseJavaClass):
    """!This class represents action for conversion of transparency."""

    java_class_name = "com.aspose.python.pdf.ConvertTransparencyAction"
    java_class = jpype.JClass(java_class_name)

    Default = java_class.Default
    """!
     Use default strategy, no adding masks.
    
    """

    Mask = java_class.Mask
    """!
     Add transparent mask image.
    
    """

