import jpype 
from asposepdf import Assist 


class IFontOptions(Assist.BaseJavaClass):
    """!Useful properties to tune Font behavior"""

    java_class_name = "com.aspose.python.pdf.IFontOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
