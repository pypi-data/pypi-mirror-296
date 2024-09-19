import jpype 
from asposepdf import Assist 


class printing_PrintPaperSourceKind(Assist.BaseJavaClass):
    """!Standard paper sources."""

    java_class_name = "com.aspose.python.pdf.printing.PrintPaperSourceKind"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

