import jpype
from asposepdf import Assist
from asposepdf.Api import Document
from asposepdf.Assist import JavaRectangle


class Facade(Assist.BaseJavaClass):
    """!
    Base facade class.
    """

    javaClassName = "com.aspose.python.pdf.facades.Facade"
    sourceFileName = None
    document = None

    def __init__(self, document: Document = None, sourceFileName: str = None):
        if document is not None:
            self.document = document
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(document.get_java_object())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            javaClass = jpype.JClass(self.javaClassName)
            self.javaClass = javaClass(sourceFileName)
        else:
            self.javaClass = jpype.JClass(self.javaClassName)()

    def get_java_object(self):
        return self.java_object

    def set_java_object(self, java_object):
        self.java_object = java_object

    def get_java_class_name(self):
        return self.javaClassName

    def bindPdf(self, document: Document = None, sourceFileName: str = None):
        """!
        Initializes the facade.
        """

        if document is not None:
            self.document = document
            self.java_object.bindPdf(document.get_java_object())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            self.java_object.bindPdf(sourceFileName)
        else:
            raise ValueError("Either 'document' or 'sourceFileName' must be specified")

    def bindPdfFile(self, sourceFileName: str, password: str = None):
        """!
        Initializes the facade from pdf protected by password.
        """

        if password is not None:
            self.sourceFileName = sourceFileName
            self.java_object.bindPdf(sourceFileName)
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            self.java_object.bindPdf(sourceFileName, password)
        else:
            raise ValueError("'sourceFileName' must be specified")


class Signature(Assist.BaseJavaClass):
    """!
    An abstract class which represents signature object in the pdf document. Signatures are fields
    with values of signature objects, the last contain data which is used to verify the document
    validity.
    """

    javaClassName = "com.aspose.python.pdf.Signature"

    def close(self):
        """!
        Destructor which closes temporary streams (if necessary).
        """
        self.java_object.close()


class PKCS7(Signature):
    """!
    Represents the PKCS#7 object that conform to the PKCS#7 specification in Internet
    RFC 2315, PKCS#7: Cryptographic Message Syntax, Version 1.5. The SHA1 digest of the document's byte range is
    encapsulated in the PKCS#7 SignedData field.
    """

    javaClassName = "com.aspose.python.pdf.PKCS7"

    def __init__(self, pfx, password):
        """!
        Initializes new instance of the Signature class.
        """
        java_class = jpype.JClass(self.javaClassName)
        self.java_object = java_class(pfx, password)


class PKCS7Detached(Signature):
    """!
    Represents the PKCS#7 object that conform to the PKCS#7 specification in Internet RFC 2315, PKCS
    #7: Cryptographic Message Syntax, Version 1.5. The original signed message digest over the
    document's byte range is incorporated as the normal PKCS#7 SignedData field. No data shall is
    encapsulated in the PKCS#7 SignedData field.
    """

    javaClassName = "com.aspose.python.pdf.PKCS7Detached"

    def __init__(self, pfx, password):
        """!
        Initializes new instance of the Signature class.
        """
        java_class = jpype.JClass(self.javaClassName)
        self.java_object = java_class(pfx, password)


class PdfFileSignature(Facade):
    """!
    Represents a class to sign a pdf file with a certificate.
    """

    javaClassName = "com.aspose.python.pdf.facades.PdfFileSignature"

    def __init__(self, document: Document = None):
        """!
        Initializes new PdfFileSignature object.
        """
        if document is None:
            java_class = jpype.JClass(self.javaClassName)
            self.java_object = java_class()
        else:
            java_class = jpype.JClass(self.javaClassName)
            self.java_object = java_class(document.get_java_object())

    @property
    def containsSignature(self):
        """!
        Checks if the pdf has a digital signature or not.
        """
        return self.java_object.containsSignature()

    @property
    def containsUsageRights(self):
        """!
        Checks if the pdf has a usage rights or not.
        """
        return self.java_object.containsUsageRights()

    @property
    def isCertified(self):
        """!
        Gets the flag determining whether a document is certified or not.
        """
        return self.java_object.isCertified()

    @property
    def isLtvEnabled(self):
        """!
        Gets the LTV enabled flag.
        """
        return self.java_object.isLtvEnabled()

    def delete(self, fieldName: str):
        """!
        Deletes field from the form by its name.
        """
        self.java_object.delete(fieldName)

    def close(self):
        """!
        Closes the facade.
        """
        self.java_object.close()

    def removeUsageRights(self):
        """!
        Removes the usage rights entry.
        """
        self.java_object.removeUsageRights()

    def setCertificate(self, pfx, password):
        """!
        Set certificate file and password for signing routine.
        Args:
        pfx (str): Path to the certificate file (PFX format).
        password (str): Password for the certificate file.
        """
        self.java_object.setCertificate(pfx, password)

    def sign(self, page: int, SigReason: str, SigContact: str, SigLocation: str, visible: bool, annotRect: JavaRectangle):
        """!
        Make a signature on the pdf document with PKCS1 certificate
        """
        self.java_object.sign(page, SigReason, SigContact, SigLocation, visible, annotRect.get_java_object())

    def signWithCertificate(self, page: int, visible: bool, annotRect: JavaRectangle, certificate: Signature):
        """!
        Make a signature on the pdf document with added certificate
        """
        self.java_object.sign(page, visible, annotRect.get_java_object(), certificate.get_java_object())

    def save(self, fileName):
        """!
        Saves the result PDF to file.
        """

        if fileName is None:
            self.get_java_object().save()
        else:
            self.get_java_object().save(fileName)


class Form(Facade):
    """!
    Class representing Acro form object.
    """

    javaClassName = "com.aspose.python.pdf.facades.Form"
    sourceFileName = None
    document = None

    def __init__(self, document: Document = None, sourceFileName: str = None):
        if document is not None:
            self.document = document
            java_class = jpype.JClass(self.javaClassName)
            self.java_object = java_class(document.get_java_object())
        elif sourceFileName is not None:
            self.sourceFileName = sourceFileName
            java_class = jpype.JClass(self.javaClassName)
            self.java_object = java_class(sourceFileName)
        else:
            self.java_object = jpype.JClass(self.javaClassName)()

    def delete(self, fieldName):
        """!
        Deletes field from the form by its name.
        """
        self.java_object.delete(fieldName)

    def flatten(self):
        """!
        Removes all static form fields and place their values directly on the page.
        """
        self.java_object.flatten()

    def hasField(self, fieldName):
        """!
        Determines if the field with specified name already added to the Form.
        """
        return self.java_object.hasField(fieldName)

    def hasXfa(self):
        """!
        Determines if the form has Xfa
        """
        return self.java_object.hasXfa()

    def isReadOnly(self):
        """!
        Determines if collection is readonly. Always returns false.
        """
        return self.java_object.isReadOnly()

    def isSignaturesExist(self):
        """!
        If set, the document contains at least one signature field.
        """
        return self.java_object.getSignaturesExist()

    def size(self):
        """!
        Gets number of the fields on this form.
        """
        return self.java_object.size()

