import jpype 
from asposepdf import Assist 


class LaTeXSaveOptions(Assist.BaseJavaClass):
    """!Save options for export to TeX format.
     
     @deprecated Use TeXSaveOptions instead"""

    java_class_name = "com.aspose.python.pdf.LaTeXSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
