import jpype 
from asposepdf import Assist 


class ApsToFlowConverter(Assist.BaseJavaClass):
    """!APS to Flow Conversion * !!! Don't port from C# as could be ahead of .Net version !!!!"""

    java_class_name = "com.aspose.python.pdf.ApsToFlowConverter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
