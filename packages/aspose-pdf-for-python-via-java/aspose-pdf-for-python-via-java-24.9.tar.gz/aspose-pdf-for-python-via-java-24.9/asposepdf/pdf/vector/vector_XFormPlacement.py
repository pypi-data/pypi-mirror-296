import jpype 
from asposepdf import Assist 


class vector_XFormPlacement(Assist.BaseJavaClass):
    """!Represents XForm placement.
     If the XForm is displayed on the page more than 1 time,
     all XformPlacements associated with this XForm will have common graphical elements, but different graphical states."""

    java_class_name = "com.aspose.python.pdf.vector.XFormPlacement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
