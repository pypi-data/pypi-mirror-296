import jpype 
from asposepdf import Assist 


class printing_PrintPaperSources(Assist.BaseJavaClass):
    """!Provides a set of predefined {@link PrintPaperSource} instances representing common paper sources.
     This class cannot be inherited."""

    java_class_name = "com.aspose.python.pdf.printing.PrintPaperSources"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

