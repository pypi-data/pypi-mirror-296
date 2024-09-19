import jpype 
from asposepdf import Assist 


class SaveOptions_NodeLevelResourceType(Assist.BaseJavaClass):
    """!enumerates possible types of saved external resources"""

    java_class_name = "com.aspose.python.pdf.SaveOptions.NodeLevelResourceType"
    java_class = jpype.JClass(java_class_name)

    Image = java_class.Image
    """!
     Means that supplied resource is image
    
    """

    Font = java_class.Font
    """!
     Means that supplied resource is font
    
    """

