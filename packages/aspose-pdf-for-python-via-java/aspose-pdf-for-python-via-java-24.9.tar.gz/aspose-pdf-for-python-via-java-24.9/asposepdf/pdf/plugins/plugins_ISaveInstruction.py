import jpype 
from asposepdf import Assist 


class plugins_ISaveInstruction(Assist.BaseJavaClass):
    """!General save instruction interface that defines common members that concrete plugin option should implement."""

    java_class_name = "com.aspose.python.pdf.plugins.ISaveInstruction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
