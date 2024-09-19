import jpype 
from asposepdf import Assist 


class tex_TeXLoadResult(Assist.BaseJavaClass):
    """!Results for TeX load and compiling."""

    java_class_name = "com.aspose.python.pdf.tex.TeXLoadResult"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Spotless = 1
    _FatalErrorStop = 4
    _InvalidResult = 5
    _WarningIssued = 2
    _NotExecuted = 0
    _ErrorMessageIssued = 3
