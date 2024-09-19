import jpype 
from asposepdf import Assist 


class printing_PrintPageSettings(Assist.BaseJavaClass):
    """!Specifies settings that apply to a single, printed page."""

    java_class_name = "com.aspose.python.pdf.printing.PrintPageSettings"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
