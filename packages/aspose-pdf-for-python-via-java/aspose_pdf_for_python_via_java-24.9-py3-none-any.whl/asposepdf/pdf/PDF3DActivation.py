import jpype 
from asposepdf import Assist 


class PDF3DActivation(Assist.BaseJavaClass):
    """!Enum PDF3DActivation: set of 3D annotation activation mode."""

    java_class_name = "com.aspose.python.pdf.PDF3DActivation"
    java_class = jpype.JClass(java_class_name)

    activeWhenOpen = java_class.activeWhenOpen
    """!
     The active when open
    
    """

    activeWhenVisible = java_class.activeWhenVisible
    """!
     The active when visible
    
    """

    activatedUserOrScriptAction = java_class.activatedUserOrScriptAction
    """!
     The activated by user or script action
    
    """

