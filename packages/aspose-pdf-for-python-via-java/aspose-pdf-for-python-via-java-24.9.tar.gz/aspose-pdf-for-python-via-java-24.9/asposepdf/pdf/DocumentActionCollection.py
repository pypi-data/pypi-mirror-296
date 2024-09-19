import jpype 
from asposepdf import Assist 


class DocumentActionCollection(Assist.BaseJavaClass):
    """!Class describes actions performed on some actions with document"""

    java_class_name = "com.aspose.python.pdf.DocumentActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
