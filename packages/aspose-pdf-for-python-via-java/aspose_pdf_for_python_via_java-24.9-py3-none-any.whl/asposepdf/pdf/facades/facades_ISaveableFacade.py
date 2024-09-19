import jpype 
from asposepdf import Assist 


class facades_ISaveableFacade(Assist.BaseJavaClass):
    """!Facade interface that defines methods common for all saveable facades."""

    java_class_name = "com.aspose.python.pdf.facades.ISaveableFacade"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
