import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_StructureTypeCategory(Assist.BaseJavaClass):
    """!Represents Categories of Standard Structure Types."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.StructureTypeCategory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

