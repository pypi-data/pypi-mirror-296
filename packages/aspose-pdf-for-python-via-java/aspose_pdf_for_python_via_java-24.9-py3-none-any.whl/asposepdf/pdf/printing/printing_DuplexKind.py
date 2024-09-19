import jpype 
from asposepdf import Assist 


class printing_DuplexKind(Assist.BaseJavaClass):
    """!Specifies the printer's duplex setting."""

    java_class_name = "com.aspose.python.pdf.printing.DuplexKind"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

