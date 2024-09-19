import jpype 
from asposepdf import Assist 


class ImportOptions(Assist.BaseJavaClass):
    """!ImportOptions type hold level of abstraction on individual import options."""

    java_class_name = "com.aspose.python.pdf.ImportOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
