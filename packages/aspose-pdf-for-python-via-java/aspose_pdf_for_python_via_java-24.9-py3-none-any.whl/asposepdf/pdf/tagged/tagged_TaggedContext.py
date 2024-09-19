import jpype 
from asposepdf import Assist 


class tagged_TaggedContext(Assist.BaseJavaClass):
    """!For internal usage only"""

    java_class_name = "com.aspose.python.pdf.tagged.TaggedContext"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
