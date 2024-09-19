import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionValueType(Assist.BaseJavaClass):
    """!The PDF/A ValueType schema is required for all property value types which are not defined in the
     XMP 2004 specification, i.e. for value types outside of the following list: - Array types (these
     are container types which may contain one or more fields): Alt, Bag, Seq - Basic value types:
     Boolean, (open and closed) Choice, Date, Dimensions, Integer, Lang Alt, Locale, MIMEType,
     ProperName, Real, Text, Thumbnail, URI, URL, XPath - Media Management value types: AgentName,
     RenditionClass, ResourceEvent, ResourceRef, Version - Basic Job/Workflow value type: Job - EXIF
     schema value types: Flash, CFAPattern, DeviceSettings, GPSCoordinate, OECF/SFR, Rational Schema
     namespace URI: http://www.aiim.org/pdfa/ns/type# Required schema namespace prefix: pdfaType"""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionValueType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
