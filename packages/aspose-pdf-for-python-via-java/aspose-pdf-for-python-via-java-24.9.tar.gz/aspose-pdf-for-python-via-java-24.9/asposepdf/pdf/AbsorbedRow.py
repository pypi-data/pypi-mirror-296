import jpype 
from asposepdf import Assist 


class AbsorbedRow(Assist.BaseJavaClass):
    """!Represents row of table that exist on the page"""

    java_class_name = "com.aspose.python.pdf.AbsorbedRow"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
