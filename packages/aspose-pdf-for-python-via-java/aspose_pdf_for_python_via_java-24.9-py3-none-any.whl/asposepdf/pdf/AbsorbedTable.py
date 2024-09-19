import jpype 
from asposepdf import Assist 


class AbsorbedTable(Assist.BaseJavaClass):
    """!Represents table that exist on the page"""

    java_class_name = "com.aspose.python.pdf.AbsorbedTable"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
