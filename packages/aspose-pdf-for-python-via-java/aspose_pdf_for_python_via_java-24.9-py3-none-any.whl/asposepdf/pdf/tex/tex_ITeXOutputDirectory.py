import jpype 
from asposepdf import Assist 


class tex_ITeXOutputDirectory(Assist.BaseJavaClass):
    """!Interface of generalized TeX output directory."""

    java_class_name = "com.aspose.python.pdf.tex.ITeXOutputDirectory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
