import jpype 
from asposepdf import Assist 


class SaveOptions(Assist.BaseJavaClass):
    """!SaveOptions type hold level of abstraction on individual save options"""

    java_class_name = "com.aspose.python.pdf.SaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
