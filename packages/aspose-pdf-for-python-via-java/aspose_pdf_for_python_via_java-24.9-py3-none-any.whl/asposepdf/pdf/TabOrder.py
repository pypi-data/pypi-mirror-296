import jpype 
from asposepdf import Assist 


class TabOrder(Assist.BaseJavaClass):
    """!Tab order on the page"""

    java_class_name = "com.aspose.python.pdf.TabOrder"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Column = 2
    _Manual = 4
    _Row = 1
    _None = 0
    _Default = 3
