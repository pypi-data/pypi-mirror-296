import jpype 
from asposepdf import Assist 


class LoadOptions_ResourceLoadingResult(Assist.BaseJavaClass):
    """!Result of custom loading of resource"""

    java_class_name = "com.aspose.python.pdf.LoadOptions.ResourceLoadingResult"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
