import jpype 
from asposepdf import Assist 


class RenderModeType(Assist.BaseJavaClass):
    """!Enum RenderModeType: set of render mode types"""

    java_class_name = "com.aspose.python.pdf.RenderModeType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _TransparentBoundingBox = 5
    _ShadedVertices = 10
    _Illustration = 11
    _Wireframe = 7
    _SolidWireframe = 1
    _ShadedIllustration = 13
    _Solid = 0
    _Vertices = 9
    _ShadedWireframe = 8
    _Transparent = 2
    _TransparentWareFrame = 3
    _BoundingBox = 4
    _TransparentBoundingBoxOutline = 6
    _SolidOutline = 12
