import jpype 
from asposepdf import Assist 


class plugins_merger_MergeOptions(Assist.BaseJavaClass):
    """!Represents Merge options for {@link Merger} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.merger.MergeOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
