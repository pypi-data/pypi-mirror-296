import jpype 
from asposepdf import Assist 


class SoundSampleDataEncodingFormat(Assist.BaseJavaClass):
    """!The encoding format for the sound sample data."""

    java_class_name = "com.aspose.python.pdf.SoundSampleDataEncodingFormat"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Signed = 1
    _Raw = 0
    _muLaw = 2
    _ALaw = 3
