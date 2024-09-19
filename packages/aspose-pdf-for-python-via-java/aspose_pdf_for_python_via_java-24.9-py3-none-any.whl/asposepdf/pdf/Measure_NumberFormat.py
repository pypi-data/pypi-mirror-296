import jpype 
from asposepdf import Assist 


class Measure_NumberFormat(Assist.BaseJavaClass):
    """!Number format for measure."""

    java_class_name = "com.aspose.python.pdf.Measure.NumberFormat"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
