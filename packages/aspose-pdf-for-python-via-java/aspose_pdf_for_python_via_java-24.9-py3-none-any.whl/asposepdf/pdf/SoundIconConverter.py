import jpype 
from asposepdf import Assist 


class SoundIconConverter(Assist.BaseJavaClass):
    """!Represents SoundIconConverter class"""

    java_class_name = "com.aspose.python.pdf.SoundIconConverter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
