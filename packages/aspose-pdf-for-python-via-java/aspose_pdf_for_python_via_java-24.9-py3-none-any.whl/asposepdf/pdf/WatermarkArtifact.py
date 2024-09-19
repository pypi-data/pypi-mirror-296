import jpype 
from asposepdf import Assist 


class WatermarkArtifact(Assist.BaseJavaClass):
    """!Class describes watermark artifact. This may be used to"""

    java_class_name = "com.aspose.python.pdf.WatermarkArtifact"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
