import jpype 
from asposepdf import Assist 


class UnifiedSaveOptions_ConversionProgressEventHandler(Assist.BaseJavaClass):
    """!Represents class with abstract method that usually supplied by calling side and handles progress events that
     comes from converter. Usually such supplied customer's handler can be used to show total
     conversion progress on console or in progress bar."""

    java_class_name = "com.aspose.python.pdf.UnifiedSaveOptions.ConversionProgressEventHandler"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
