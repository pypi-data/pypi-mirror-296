import jpype 
from asposepdf import Assist 


class ConvertSoftMaskAction(Assist.BaseJavaClass):
    """!This action represents actions for conversion of images with soft mask."""

    java_class_name = "com.aspose.python.pdf.ConvertSoftMaskAction"
    java_class = jpype.JClass(java_class_name)

    Default = java_class.Default
    """!
     Use default strategy.
    
    """

    ConvertToStencilMask = java_class.ConvertToStencilMask
    """!
     Soft mask will be converted into stencil mask.
    
    """

