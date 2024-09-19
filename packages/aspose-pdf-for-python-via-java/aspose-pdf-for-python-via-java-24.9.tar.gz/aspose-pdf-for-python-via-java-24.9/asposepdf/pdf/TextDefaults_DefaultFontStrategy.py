import jpype 
from asposepdf import Assist 


class TextDefaults_DefaultFontStrategy(Assist.BaseJavaClass):
    """!Specifies type of text subsystem defaults"""

    java_class_name = "com.aspose.python.pdf.TextDefaults.DefaultFontStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _SystemFont = 0
    _PredefinedFont = 1
    _TheFirstSuitableFoundFont = 3
    _ListOfFonts = 2
