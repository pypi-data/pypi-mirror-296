import jpype 
from asposepdf import Assist 


class UnifiedSaveOptions_ProgressEventHandlerInfo(Assist.BaseJavaClass):
    """!This class represents information about conversion progress that can be used in external
     application to show conversion progress to end user"""

    java_class_name = "com.aspose.python.pdf.UnifiedSaveOptions.ProgressEventHandlerInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
