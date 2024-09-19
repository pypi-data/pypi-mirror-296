import jpype 
from asposepdf import Assist 


class XmlSaveOptions(Assist.BaseJavaClass):
    """!Save options for export to Xml format"""

    java_class_name = "com.aspose.python.pdf.XmlSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
