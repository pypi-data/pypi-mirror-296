import jpype 
from asposepdf import Assist 


class IIndexBitmapConverterInternal(Assist.BaseJavaClass):
    """!This interface declared for customization algorithms of quantization. Users can implement their
     own realization of this algorithms (for example algorithms based on unmanaged code)."""

    java_class_name = "com.aspose.python.pdf.IIndexBitmapConverterInternal"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
