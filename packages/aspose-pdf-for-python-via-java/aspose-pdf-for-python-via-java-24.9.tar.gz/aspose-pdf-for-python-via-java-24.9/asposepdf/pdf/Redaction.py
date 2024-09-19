import jpype 
from asposepdf import Assist 


class Redaction(Assist.BaseJavaClass):
    """!For internal usage only
     @author User"""

    java_class_name = "com.aspose.python.pdf.Redaction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
