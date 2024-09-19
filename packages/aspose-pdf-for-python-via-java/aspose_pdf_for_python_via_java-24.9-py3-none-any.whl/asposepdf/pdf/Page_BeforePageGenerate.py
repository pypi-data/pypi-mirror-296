import jpype 
from asposepdf import Assist 


class Page_BeforePageGenerate(Assist.BaseJavaClass):
    """!Procedure for customize header and footer."""

    java_class_name = "com.aspose.python.pdf.Page.BeforePageGenerate"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
