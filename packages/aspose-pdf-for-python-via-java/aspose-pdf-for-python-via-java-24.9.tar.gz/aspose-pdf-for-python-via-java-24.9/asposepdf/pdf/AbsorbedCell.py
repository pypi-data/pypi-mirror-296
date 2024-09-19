import jpype 
from asposepdf import Assist 


class AbsorbedCell(Assist.BaseJavaClass):
    """!Represents cell of table that exist on the page"""

    java_class_name = "com.aspose.python.pdf.AbsorbedCell"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
