import jpype 
from asposepdf import Assist 


class plugins_pdfhtml_PdfHtml(Assist.BaseJavaClass):
    """!Represents {@link PdfHtml} plugin.
     
     The example demonstrates how to convert PDF to HTML document.
     // create PdfHtml
     PdfHtml converter = new PdfHtml();
     // create PdfToHtmlOptions object to set output data type as file with embedded resources
     PdfToHtmlOptions opt = new PdfToHtmlOptions(PdfToHtmlOptions.SaveDataType.FileWithEmbeddedResources);
     // add input file path
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     converter.Process(opt);
     The example demonstrates how to convert HTML to PDF document.
     
     // create PdfHtml
     PdfHtml converter = new PdfHtml();
     // create HtmlToPdfOptions
     HtmlToPdfOptions opt = new HtmlToPdfOptions();
     // add input file path
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     converter.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.pdfhtml.PdfHtml"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
