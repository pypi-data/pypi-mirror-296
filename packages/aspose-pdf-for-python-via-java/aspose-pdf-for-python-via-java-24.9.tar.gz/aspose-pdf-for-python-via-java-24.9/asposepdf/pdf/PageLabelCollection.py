import jpype 
from asposepdf import Assist 


class PageLabelCollection(Assist.BaseJavaClass):
    """!Class represeingting page label collection."""

    java_class_name = "com.aspose.python.pdf.PageLabelCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
