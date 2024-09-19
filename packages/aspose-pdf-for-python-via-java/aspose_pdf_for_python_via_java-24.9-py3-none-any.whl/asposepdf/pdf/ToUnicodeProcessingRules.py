import jpype 
from asposepdf import Assist 


class ToUnicodeProcessingRules(Assist.BaseJavaClass):
    """!This class describes rules which can be used to solve Adobe Preflight error
     "Text cannot be mapped to Unicode"."""

    java_class_name = "com.aspose.python.pdf.ToUnicodeProcessingRules"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
