import jpype 
from asposepdf import Assist 


class SoundSampleData(Assist.BaseJavaClass):
    """!Represents additional entries specific to a sound object (Section 9.2 PDF1-7)"""

    java_class_name = "com.aspose.python.pdf.SoundSampleData"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DEFAULT_SAMPLING_RATE = 11025
    _DEFAULT_OF_BITS_PER_CHANNEL = 8
    _DEFAULT_OF_SOUND_CHANNELS = 1
