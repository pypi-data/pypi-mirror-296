import jpype 
from asposepdf import Assist 


class ImagePlacementCollection(Assist.BaseJavaClass):
    """!Represents an image placements collection"""

    java_class_name = "com.aspose.python.pdf.ImagePlacementCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
