import jpype 
from asposepdf import Assist 


class plugins_pdfextractor_PdfExtractor(Assist.BaseJavaClass):
    """!Represents base functionality to extract text, images, and other types of content that may occur on the pages of PDF documents.
     
     The example demonstrates how to extract text content of PDF document.
     // create PdfExtractor object to extract PDF contents
     TextExtractor extractor = new TextExtractor();
     {
     // create TextExtractorOptions object to set instructions
     TextExtractorOptions extractorOptions = new TextExtractorOptions();
     // add input file path to data sources
     extractorOptions.addInput(new FileDataSource(inputPath));
     // perform extraction process
     ResultContainer resultContainer = extractor.process(extractorOptions);
     // get the extracted text from the ResultContainer object
     string textExtracted = resultContainer.getResultCollection().get(0).toString();
     }
     The {@link TextExtractor} object is used to extract text, or {@link ImageExtractor} to extract images."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfextractor.PdfExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
