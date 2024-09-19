import jpype 
from asposepdf import Assist 


class comparison_EditOperationsOrder(Assist.BaseJavaClass):
    """!Specifies the order of edit operations."""

    java_class_name = "com.aspose.python.pdf.comparison.EditOperationsOrder"
    java_class = jpype.JClass(java_class_name)

    InsertFirst = java_class.InsertFirst
    """!
     Insert operations before delete operations.
    
    """

    DeleteFirst = java_class.DeleteFirst
    """!
     Delete operations before insert operations.
    
    """

