import importlib.util
import os
import sys
from abc import ABC

class PluginBase(ABC):
    """ Plugin Base class for implementing Statiq Plugins
    """
    
    def __init__(self, *args, **kwargs):
        pass
    
    def pre_data(self, *args, **kwargs):
        """ Called before data is loaded
        """
        raise NotImplementedError
    
    def post_data(self, data, *args, **kwargs):
        """ Called after data is loaded
        """
        raise NotImplementedError
    
    def pre_head(self, *args, **kwargs):
        """ Called before head is rendered
        """
        raise NotImplementedError
    
    def post_head(self, head, *args, **kwargs):
        """ Called after head is rendered
        """
        raise NotImplementedError
    
    def pre_render(self, *args, **kwargs):
        """ Called before rendering
        """
        raise NotImplementedError
    
    def post_render(self, html, *args, **kwargs):
        """ Called after rendering
        """
        raise NotImplementedError


class FileHandler(ABC):
    """ File Handler Base class for implementing Statiq File Handlers
        Handles file discovery from config.STATIC_PATHS
        Handles file copying to output directory
    """
        
    def __init__(self, *args, **kwargs):
        self.config = self._load_config()
        pass
    
    def _load_config(self):
        # load config.py from the root of the project
        config_path = os.path.join(os.getcwd(), "config.py")
        if not os.path.exists(config_path):
            return {}
        spec = importlib.util.spec_from_file_location("config", config_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["config"] = module
        spec.loader.exec_module(module)
        return module
    
    def parse(self):
        """ Parse files from config.STATIC_PATHS
        """
        raise NotImplementedError
    
    def copy(self):
        """ Copy files to output directory
        """
        raise NotImplementedError