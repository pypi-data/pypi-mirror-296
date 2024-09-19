import jpype 
from asposepdf import Assist 


class plugins_splitter_SplitOptions(Assist.BaseJavaClass):
    """!Represents Split options for {@link Splitter} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.splitter.SplitOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
