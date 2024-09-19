import jpype 
from asposepdf import Assist 


class LoadOptions_ResourceLoadingStrategy(Assist.BaseJavaClass):
    """!Sometimes it's necessary to avoid usage of internal loader of external resources(like images
     or CSSes) and supply custom method, that will get requested resources from somewhere. For
     example during usage of Aspose.PDf in cloud direct access to referenced files impossible, and
     some custom code put into special method should be used. This delegate defines signature of
     such custom method."""

    java_class_name = "com.aspose.python.pdf.LoadOptions.ResourceLoadingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
