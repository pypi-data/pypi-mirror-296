import jpype 
from asposepdf import Assist 


class ProgressEventType(Assist.BaseJavaClass):
    """!This enum describes possible progress event types that can occure during conversion"""

    java_class_name = "com.aspose.python.pdf.ProgressEventType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _TotalProgress = 0
    _SourcePageAnalysed = 1
    _ResultPageCreated = 2
    _ResultPageSaved = 3
