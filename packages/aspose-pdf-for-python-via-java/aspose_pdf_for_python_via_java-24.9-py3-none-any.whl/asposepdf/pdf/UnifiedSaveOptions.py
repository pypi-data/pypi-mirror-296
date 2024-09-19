import jpype 
from asposepdf import Assist 


class UnifiedSaveOptions(Assist.BaseJavaClass):
    """!This class represents saving options for saving that uses unified conversion way (with unified
     internal document model)"""

    java_class_name = "com.aspose.python.pdf.UnifiedSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

