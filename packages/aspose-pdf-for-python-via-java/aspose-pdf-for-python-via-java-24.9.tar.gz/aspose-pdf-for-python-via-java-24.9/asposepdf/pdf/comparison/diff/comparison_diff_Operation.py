import jpype 
from asposepdf import Assist 


class comparison_diff_Operation(Assist.BaseJavaClass):
    """!Represents a difference operation type."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.Operation"
    java_class = jpype.JClass(java_class_name)

    Equal = java_class.Equal
    """!
     The equal operation.
    
    """

    Delete = java_class.Delete
    """!
     The delete operation.
    
    """

    Insert = java_class.Insert
    """!
     The insert operation.
    
    """

