import jpype 
from asposepdf import Assist 


class BaseActionCollection(Assist.BaseJavaClass):
    """!Class encapsulates basic actions with page/annotation/field interactive actions"""

    java_class_name = "com.aspose.python.pdf.BaseActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
