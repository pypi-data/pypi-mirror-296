import jpype 
from asposepdf import Assist 


class FormattedFragment(Assist.BaseJavaClass):
    """!Represents abstract formatted fragment."""

    java_class_name = "com.aspose.python.pdf.FormattedFragment"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
