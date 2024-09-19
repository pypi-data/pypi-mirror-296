import jpype 
from asposepdf import Assist 


class XslFoLoadOptions_ParsingErrorsHandlingTypes(Assist.BaseJavaClass):
    """!Source XSLFO document can contain formatting errors. This enum enumerates possible strategies
     of handling of such formatting errors"""

    java_class_name = "com.aspose.python.pdf.XslFoLoadOptions.ParsingErrorsHandlingTypes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _TryIgnore = 0
    _InvokeCustomHandler = 2
    _ThrowExceptionImmediately = 1
