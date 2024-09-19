import jpype 
from asposepdf import Assist 


class FileSelectBoxField(Assist.BaseJavaClass):
    """!Field for file select box element."""

    java_class_name = "com.aspose.python.pdf.FileSelectBoxField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
