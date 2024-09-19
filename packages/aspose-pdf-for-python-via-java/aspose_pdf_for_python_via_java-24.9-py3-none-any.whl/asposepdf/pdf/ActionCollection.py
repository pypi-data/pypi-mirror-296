import jpype 
from asposepdf import Assist 


class ActionCollection(Assist.BaseJavaClass):
    """!Collection of actions"""

    java_class_name = "com.aspose.python.pdf.ActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
