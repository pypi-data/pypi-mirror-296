import jpype 
from asposepdf import Assist 


class Document_RepairOptions(Assist.BaseJavaClass):
    """!Represents options for repairing a PDF document.
     This class provides a way to customize the repair process of a PDF document."""

    java_class_name = "com.aspose.python.pdf.Document.RepairOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
