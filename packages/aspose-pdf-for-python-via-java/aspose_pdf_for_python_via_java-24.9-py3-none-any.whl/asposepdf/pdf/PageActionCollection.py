import jpype 
from asposepdf import Assist 


class PageActionCollection(Assist.BaseJavaClass):
    """!This class describes page actions"""

    java_class_name = "com.aspose.python.pdf.PageActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
