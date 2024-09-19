import jpype 
from asposepdf import Assist 


class ConvertErrorAction(Assist.BaseJavaClass):
    """!This class represents action for conversion errors."""

    java_class_name = "com.aspose.python.pdf.ConvertErrorAction"
    java_class = jpype.JClass(java_class_name)

    Delete = java_class.Delete
    """!
     Delete convert errors
    
    """

    Nothing = 1 #get element java_class.getByValue(1) None is reserved word in python - replaced to Nothing
    """!
     Do nothing with convert errors
    
    """

