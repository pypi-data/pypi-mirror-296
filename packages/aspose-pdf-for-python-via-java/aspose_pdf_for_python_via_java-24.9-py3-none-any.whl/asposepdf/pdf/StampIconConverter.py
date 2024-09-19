import jpype 
from asposepdf import Assist 


class StampIconConverter(Assist.BaseJavaClass):
    """!Represents StampIconConverter class"""

    java_class_name = "com.aspose.python.pdf.StampIconConverter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
