import jpype 
from asposepdf import Assist 


class Copier(Assist.BaseJavaClass):
    """!Class for coping object"""

    java_class_name = "com.aspose.python.pdf.Copier"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
