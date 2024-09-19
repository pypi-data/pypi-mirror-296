import jpype 
from asposepdf import Assist 


class WarningType(Assist.BaseJavaClass):
    """!Enum represented warning type."""

    java_class_name = "com.aspose.python.pdf.WarningType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _MajorFormattingLoss = 2
    _DataLoss = 1
    _MinorFormattingLoss = 3
    _SourceFileCorruption = 0
    _UnexpectedContent = 99
    _CompatibilityIssue = 4
    _InvalidInputStreamType = 5
