import jpype 
from asposepdf import Assist 


class PrinterMarksKind(Assist.BaseJavaClass):
    """!Specifies the types of printer's marks to be added to a document.
     
     This enumeration has a {@link FlagsAttribute} attribute that allows a bitwise combination of its member values."""

    java_class_name = "com.aspose.python.pdf.PrinterMarksKind"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _None = 0
