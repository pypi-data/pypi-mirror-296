import jpype 
from asposepdf import Assist 


class facades_AlignmentType(Assist.BaseJavaClass):
    """!Class contains possibly alignment types. </br>
     Use HorizontalAlignment instead"""

    java_class_name = "com.aspose.python.pdf.facades.AlignmentType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

