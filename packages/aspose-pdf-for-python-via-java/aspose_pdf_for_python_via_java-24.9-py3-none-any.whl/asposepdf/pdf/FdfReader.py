import jpype 
from asposepdf import Assist 


class FdfReader(Assist.BaseJavaClass):
    """!Class which performs reading of FDF format.
     Document doc = new Document("example.pdf");
     InputStream fdfStream = FileInputStream("file.fdf");
     FdfReader.readAnnotations(fdfStream, doc);
     fdfStream.close();
     doc.save("example_out.pdf");"""

    java_class_name = "com.aspose.python.pdf.FdfReader"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)
