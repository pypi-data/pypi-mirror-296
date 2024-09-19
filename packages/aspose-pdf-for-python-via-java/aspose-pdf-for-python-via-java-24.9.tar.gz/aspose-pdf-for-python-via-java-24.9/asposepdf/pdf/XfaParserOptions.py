import jpype 
from asposepdf import Assist 


class XfaParserOptions(Assist.BaseJavaClass):
    """!class to handle related data encapsulation"""

    java_class_name = "com.aspose.python.pdf.XfaParserOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
