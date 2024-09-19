import jpype 
from asposepdf import Assist 


class LoadOptions_MarginsAreaUsageModes(Assist.BaseJavaClass):
    """!Represents mode of usage of margins area during conversion (like HTML, EPUB etc), defines
     treatement of instructions of imported format related to usage of margins."""

    java_class_name = "com.aspose.python.pdf.LoadOptions.MarginsAreaUsageModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _PutContentOnMarginAreaIfNecessary = 0
    _NeverPutContentOnMarginArea = 1
