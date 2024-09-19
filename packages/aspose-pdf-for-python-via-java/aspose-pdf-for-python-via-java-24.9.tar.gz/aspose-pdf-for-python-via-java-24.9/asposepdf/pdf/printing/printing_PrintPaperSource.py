import jpype 
from asposepdf import Assist 


class printing_PrintPaperSource(Assist.BaseJavaClass):
    """!Specifies the paper tray from which the printer gets paper."""

    java_class_name = "com.aspose.python.pdf.printing.PrintPaperSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
