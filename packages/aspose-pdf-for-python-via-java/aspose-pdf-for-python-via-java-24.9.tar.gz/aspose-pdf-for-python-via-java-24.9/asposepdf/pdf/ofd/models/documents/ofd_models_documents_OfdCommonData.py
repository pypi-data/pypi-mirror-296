import jpype 
from asposepdf import Assist 


class ofd_models_documents_OfdCommonData(Assist.BaseJavaClass):
    """!Xml parser for {@link OfdCommonData}"""

    java_class_name = "com.aspose.python.pdf.ofd.models.documents.OfdCommonData"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
