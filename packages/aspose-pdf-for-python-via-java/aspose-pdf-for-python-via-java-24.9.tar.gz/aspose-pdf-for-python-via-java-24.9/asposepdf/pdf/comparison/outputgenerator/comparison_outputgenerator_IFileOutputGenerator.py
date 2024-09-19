import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_IFileOutputGenerator(Assist.BaseJavaClass):
    """!Represents an interface for generating output to a file of differences between texts."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.IFileOutputGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
