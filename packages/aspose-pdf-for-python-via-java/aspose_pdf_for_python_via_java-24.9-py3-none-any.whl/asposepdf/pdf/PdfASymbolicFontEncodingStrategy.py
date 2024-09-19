import jpype 
from asposepdf import Assist 


class PdfASymbolicFontEncodingStrategy(Assist.BaseJavaClass):
    """!This class describes rules which can be used to tune process of copying encoding data for cases
     when TrueType symbolic font has more than one encoding.
     Some PDF documents after conversion into PDF/A format could give an error
     "More than one encoding in symbolic TrueType font's cmap".
     What is a reason of this error? All TrueType symbolic fonts have special table "cmap"
     in it's internal data. This table maps character codes to glyph indices.
     And this table could contain different encoding subtables which
     describe encodings used. See advanced info about cmap tables at
     https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6cmap.html.
     Usually cmap table contains several encoding subtables, but PDF/A standard requires
     that either only one encoding subtable must be left for this font in PDF/A document
     or there must be a (3,0) encoding subtable among this font subtables.
     And key question here - what data must be taken from another subtables to copy into
     destination encoding table (3,0)? Majority of fonts have 'well-formed' cmap tables where
     every encoding subtable is fully consistent with another subtable. But some fonts
     have cmap tables with collisions - where for example one subtable has glyph index
     100 for unicode 100, but another subtable has glyph index 200 for the same unicode 100.
     To solve this problems special strategy needed.
     By default following strategy used:
     mac subtable(1,0) is looked for. If this table is found, only this data used to fill destination
     table (3,0). If mac subtable is not found then all subtables except (3,0) are iterated
     and used to copy data into destination (3,0) subtable. Also mapping for every unicode(unicode, glyph index)
     is copied into destination table only if destination table does not have this unicode at current moment.
     So, for example if first subtabe has glyph index 100 for unicode 100, and next subtable has glyph
     index 200 for the same unicode 100, only data from first subtable (unicode=100, glyph index = 100) will be copied.
     So each previous subtable takes precedence over the next.
     Properties of this class { PdfASymbolicFontEncodingStrategy} help tune default behaviour.
     If property {PreferredCmapEncodingTable}({ PdfASymbolicFontEncodingStrategy#getPreferredCmapEncodingTable}/
     { PdfASymbolicFontEncodingStrategy#setPreferredCmapEncodingTable}) of type { PdfASymbolicFontEncodingStrategy.QueueItem.CMapEncodingTableType}
     is set, then relevant subtable will be used in precedence to mac subtable(1,0). Value 'MacTable' from
     enumeration {PdfASymbolicFontEncodingStrategy.QueueItem.CMapEncodingTableType} has no sense in this case, cause it
     points on the same mac subtable (1,0) which will be used by default.
     Property {CmapEncodingTablesPriorityQueue}({ PdfASymbolicFontEncodingStrategy#getCmapEncodingTablesPriorityQueue}/
     {PdfASymbolicFontEncodingStrategy#setCmapEncodingTablesPriorityQueue}) discards all priorities for any subtable.
     If this property is set, then only subtables from declared queue will be used in specified order.
     If subtables specified are not found then default iteration of all subtables and copy strategy described above
     will be used.
     Object { PdfASymbolicFontEncodingStrategy.QueueItem} specifies encoding subtable used. This subtable can be set
     via combination of members(PlatformID, PlatformSpecificId) or via { PdfASymbolicFontEncodingStrategy.QueueItem.CMapEncodingTableType}
     enumeration.
     In case when the font has no (3,0) subtable some other subtable will be used to maintain the PDF/A compatibility.
     The choice of the subtable to use is made under the same rules as described earlier, so that
     {@code PreferredCmapEncodingTable}({ PdfASymbolicFontEncodingStrategy#getPreferredCmapEncodingTable}/
     {PdfASymbolicFontEncodingStrategy#setPreferredCmapEncodingTable})
     and {@code CmapEncodingTablesPriorityQueue}({ PdfASymbolicFontEncodingStrategy#getCmapEncodingTablesPriorityQueue}/
     { PdfASymbolicFontEncodingStrategy#setCmapEncodingTablesPriorityQueue}) properties
     are used to determine the resultant subtable, and if the font doesn't have the requested subtable(s) either
     then any existent subtable will be used."""

    java_class_name = "com.aspose.python.pdf.PdfASymbolicFontEncodingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
