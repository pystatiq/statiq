
import os
import re
from statiq.abstract import FileHandler

class StaticFileHandler(FileHandler):
    """ Handles file discovery from config.STATIC_PATHS
        Handles file copying to output directory
    """
        
    def __init__(self, *args, **kwargs):
        self.config = self._load_config()
        pass
    
    def parse(self):
        """ Parse files from config.STATIC_PATHS
        """
        output_path = os.path.join(os.getcwd(), self.config.STATIC_OUTPUT_PATH)
        for static_path_config in self.config.STATIC_PATHS:
            static_path = os.path.join(os.getcwd(), static_path_config.get("path", None))
            regex = static_path_config.get("regex", None)
            if regex:
                for root, _, files in os.walk(static_path):
                    for file in files:
                        if re.match(regex, file):
                            yield os.path.join(root, file), os.path.join(root, file).replace(static_path, output_path)
            elif os.path.isdir(static_path):
                for root, _, files in os.walk(static_path):
                    for file in files:
                        yield os.path.join(root, file), os.path.join(root, file).replace(static_path, output_path)
            else:
                yield static_path, static_path.replace(os.getcwd(), output_path)
    
    def copy(self):
        """ Copy files to output directory
        """
        for source, target in self.parse():
            os.makedirs(target, exist_ok=True)
            with open(source, "rb") as f:
                content = f.read()
            with open(source, "wb") as f:
                f.write(content)