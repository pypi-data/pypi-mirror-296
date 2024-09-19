import jpype 
from asposepdf import Assist 


class PDF3DAnnotation(Assist.BaseJavaClass):
    """!Class PDF3DAnnotation. This class cannot be inherited.
     
     @see Annotation"""

    java_class_name = "com.aspose.python.pdf.PDF3DAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
