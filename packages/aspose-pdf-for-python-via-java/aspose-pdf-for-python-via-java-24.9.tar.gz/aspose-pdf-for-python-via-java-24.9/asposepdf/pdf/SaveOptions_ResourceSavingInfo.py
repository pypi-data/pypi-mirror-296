import jpype 
from asposepdf import Assist 


class SaveOptions_ResourceSavingInfo(Assist.BaseJavaClass):
    """!This class represents set of data that related to external resource file's saving that
     occures during conversion of PDF to some other format (f.e. HTML)"""

    java_class_name = "com.aspose.python.pdf.SaveOptions.ResourceSavingInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
