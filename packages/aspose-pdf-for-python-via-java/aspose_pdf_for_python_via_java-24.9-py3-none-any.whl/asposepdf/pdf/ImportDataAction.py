import jpype 
from asposepdf import Assist 


class ImportDataAction(Assist.BaseJavaClass):
    """!Upon invocation of an import-data action, Forms Data Format (FDF) data shall be imported into the document's interactive form from a specified file."""

    java_class_name = "com.aspose.python.pdf.ImportDataAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
