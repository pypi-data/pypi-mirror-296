import jpype 
from asposepdf import Assist 


class tex_TeXFileSystemOutputDirectory(Assist.BaseJavaClass):
    """!Implements the regular file system's method for getting a file stream to write to."""

    java_class_name = "com.aspose.python.pdf.tex.TeXFileSystemOutputDirectory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
