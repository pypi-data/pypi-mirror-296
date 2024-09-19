import jpype 
from asposepdf import Assist 


class LatexFragment(Assist.BaseJavaClass):
    """!Represents TeX fragment.
     
     @deprecated Please use TeXFragment instead"""

    java_class_name = "com.aspose.python.pdf.LatexFragment"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
