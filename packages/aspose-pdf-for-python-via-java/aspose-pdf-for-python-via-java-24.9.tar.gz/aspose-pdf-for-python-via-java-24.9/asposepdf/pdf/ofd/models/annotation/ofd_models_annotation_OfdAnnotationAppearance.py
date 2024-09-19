import jpype 
from asposepdf import Assist 


class ofd_models_annotation_OfdAnnotationAppearance(Assist.BaseJavaClass):
    """!Xml parser for {@link OfdAnnotationAppearance}"""

    java_class_name = "com.aspose.python.pdf.ofd.models.annotation.OfdAnnotationAppearance"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
