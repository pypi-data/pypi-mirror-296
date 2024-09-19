import jpype 
from asposepdf import Assist 


class Document_OptimizationOptions(Assist.BaseJavaClass):
    """!Class which describes document optimization algorithm. Instance of this class may be used as
     parameter of OptimizeResources() method.
     
     @deprecated This class is obsolete. Please use com.aspose.pdf.optimization.OptimizationOptions instead."""

    java_class_name = "com.aspose.python.pdf.Document.OptimizationOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
