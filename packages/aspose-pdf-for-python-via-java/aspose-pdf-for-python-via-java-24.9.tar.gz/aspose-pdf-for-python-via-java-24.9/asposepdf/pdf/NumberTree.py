import jpype 
from asposepdf import Assist 


class NumberTree(Assist.BaseJavaClass):
    """!Class representing Number tree structure of PDF file. 7.9.7Number Trees"""

    java_class_name = "com.aspose.python.pdf.NumberTree"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
