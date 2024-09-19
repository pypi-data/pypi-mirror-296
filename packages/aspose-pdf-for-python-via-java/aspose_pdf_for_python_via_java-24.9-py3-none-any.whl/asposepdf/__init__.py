import jpype
import os

__version__ = "24.9"
__version_info__ = __version__.split('.')
__asposepdf_dir__ = os.path.dirname(__file__)
__pdf_jar_path__ = __asposepdf_dir__ + "/jlib/aspose.pdf-python-24.9.jar"
jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=%s" % __pdf_jar_path__)

