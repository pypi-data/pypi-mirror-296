import jpype 
from asposepdf import Assist 


class ImageDeleteAction(Assist.BaseJavaClass):
    """!Action which performed with image object when image is removed from collection. If image object is removed"""

    java_class_name = "com.aspose.python.pdf.ImageDeleteAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _KeepContents = 0
    _Check = 3
    _ForceDelete = 2
    _None = 1
