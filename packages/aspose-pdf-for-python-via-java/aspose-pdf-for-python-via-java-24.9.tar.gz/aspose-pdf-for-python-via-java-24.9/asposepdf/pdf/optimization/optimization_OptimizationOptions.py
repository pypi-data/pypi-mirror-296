import jpype 
from asposepdf import Assist 


class optimization_OptimizationOptions(Assist.BaseJavaClass):
    """!Class which describes document optimization algorithm.
     Instance of this class may be used as parameter of OptimizeResources() method."""

    java_class_name = "com.aspose.python.pdf.optimization.OptimizationOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
