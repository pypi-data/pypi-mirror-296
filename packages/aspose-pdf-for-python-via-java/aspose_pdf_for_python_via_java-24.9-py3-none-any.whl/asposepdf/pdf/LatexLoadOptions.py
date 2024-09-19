import jpype 
from asposepdf import Assist 


class LatexLoadOptions(Assist.BaseJavaClass):
    """!Represents options for loading/importing TeX file into PDF document.
     
     @deprecated Use TeXLoadOptions instead."""

    java_class_name = "com.aspose.python.pdf.LatexLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
