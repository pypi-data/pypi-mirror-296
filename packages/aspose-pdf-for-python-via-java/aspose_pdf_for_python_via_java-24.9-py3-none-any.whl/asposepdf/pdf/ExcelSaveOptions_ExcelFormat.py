import jpype 
from asposepdf import Assist 


class ExcelSaveOptions_ExcelFormat(Assist.BaseJavaClass):
    """!Allows to specify .xls/xml or .xlsx file format. Default value is XLSX;"""

    java_class_name = "com.aspose.python.pdf.ExcelSaveOptions.ExcelFormat"
    java_class = jpype.JClass(java_class_name)

    XMLSpreadSheet2003 = java_class.XMLSpreadSheet2003
    """!
     Excel 2003 XML Format
    
    """

    XLSX = java_class.XLSX
    """!
     Office Open XML (.xlsx) File Format
    
    """

    CSV = java_class.CSV
    """!
     A comma-separated values (CSV) File Format
    
    """

    XLSM = java_class.XLSM
    """!
     A macro-enabled Office Open XML (.xlsm) File Format
    
    """

    ODS = java_class.ODS
    """!
     OpenDocument Spreadsheet
    
    """

