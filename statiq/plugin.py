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