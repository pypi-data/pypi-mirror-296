import jpype 
from asposepdf import Assist 


class PclLoadOptions_ConversionEngines(Assist.BaseJavaClass):
    """!Enumerates conversion engines that can be used for conversion"""

    java_class_name = "com.aspose.python.pdf.PclLoadOptions.ConversionEngines"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _NewEngine = 1
    _LegacyEngine = 0
