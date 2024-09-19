import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_StructureTextState(Assist.BaseJavaClass):
    """!Represents text state settings for Text Structure Elements and TaggedContent (ITextElement, ITaggedContent)"""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.StructureTextState"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
