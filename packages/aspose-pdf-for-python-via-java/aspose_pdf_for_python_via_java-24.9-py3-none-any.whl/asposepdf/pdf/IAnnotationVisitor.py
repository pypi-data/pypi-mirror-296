import jpype 
from asposepdf import Assist 


class IAnnotationVisitor(Assist.BaseJavaClass):
    """!Defines Visitor for visiting different document annotations."""

    java_class_name = "com.aspose.python.pdf.IAnnotationVisitor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
