import jpype 
from asposepdf import Assist 


class ContentsAppender(Assist.BaseJavaClass):
    """!Performs contents modifications in APPEND mode only.
     this mode allows to avoid unneeded and heavy contents parsing before some change is made to the contents.
     It only appends new operators to the end or to the begin of the contents"""

    java_class_name = "com.aspose.python.pdf.ContentsAppender"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
