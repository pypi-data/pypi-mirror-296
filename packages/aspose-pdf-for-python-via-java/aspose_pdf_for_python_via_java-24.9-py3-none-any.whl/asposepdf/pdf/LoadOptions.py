import jpype 
from asposepdf import Assist 


class LoadOptions(Assist.BaseJavaClass):
    """!LoadOptions type holds level of abstraction on individual load options"""

    java_class_name = "com.aspose.python.pdf.LoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
