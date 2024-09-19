import jpype 
from asposepdf import Assist 


class facades_StampType(Assist.BaseJavaClass):
    """!Describes stamp types."""

    java_class_name = "com.aspose.python.pdf.facades.StampType"
    java_class = jpype.JClass(java_class_name)

    Form = java_class.Form
    """!
     Stamp if Form.
    
    """

    Image = java_class.Image
    """!
     Stamp is image.
    
    """

