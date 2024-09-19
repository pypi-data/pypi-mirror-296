import jpype 
from asposepdf import Assist 


class DocumentFactory(Assist.BaseJavaClass):
    """!Class which allows to create/load documents of different types."""

    java_class_name = "com.aspose.python.pdf.DocumentFactory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
