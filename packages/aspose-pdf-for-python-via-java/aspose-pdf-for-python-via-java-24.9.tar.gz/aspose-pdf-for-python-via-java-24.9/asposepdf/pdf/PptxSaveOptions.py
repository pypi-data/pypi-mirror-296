import jpype 
from asposepdf import Assist 


class PptxSaveOptions(Assist.BaseJavaClass):
    """!Save options for export to SVG format"""

    java_class_name = "com.aspose.python.pdf.PptxSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
