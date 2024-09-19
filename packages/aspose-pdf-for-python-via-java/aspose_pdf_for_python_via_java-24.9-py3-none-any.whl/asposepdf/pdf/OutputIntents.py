import jpype 
from asposepdf import Assist 


class OutputIntents(Assist.BaseJavaClass):
    """!Represents the collection of {@link OutputIntent}."""

    java_class_name = "com.aspose.python.pdf.OutputIntents"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
