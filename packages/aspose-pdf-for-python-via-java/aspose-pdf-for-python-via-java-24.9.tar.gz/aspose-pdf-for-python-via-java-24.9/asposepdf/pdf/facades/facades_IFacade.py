import jpype 
from asposepdf import Assist 


class facades_IFacade(Assist.BaseJavaClass):
    """!General facade interface that defines common facades methods."""

    java_class_name = "com.aspose.python.pdf.facades.IFacade"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
