import jpype 
from asposepdf import Assist 


class TeXMemoryOutputDirectory(Assist.BaseJavaClass):
    """!Implements fetching an output stream from memory. You can use it, for example,
     when you don't want the accompanying output (like a log file) to be written to
     disk but you'd like to read it afterwards from memory."""

    java_class_name = "com.aspose.python.pdf.TeXMemoryOutputDirectory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
