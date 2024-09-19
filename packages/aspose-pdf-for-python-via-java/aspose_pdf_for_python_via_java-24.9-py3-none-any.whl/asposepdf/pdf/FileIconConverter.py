import jpype 
from asposepdf import Assist 


class FileIconConverter(Assist.BaseJavaClass):
    """!Represents FileIconConverter class"""

    java_class_name = "com.aspose.python.pdf.FileIconConverter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
