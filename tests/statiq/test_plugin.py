import pytest
from abc import ABC
from statiq import PluginBase

class ExamplePlugin(PluginBase):
    pass

class ExamplePluginWithParams(PluginBase):
    def __init__(self, *args, **kwargs):
        self.foo = args[0]
        self.bar = kwargs.get("bar", None)

class ExamplePluginWithAllMethods(PluginBase):
    def pre_data(self, *args, **kwargs):
        pass
    
    def post_data(self, data, *args, **kwargs):
        pass
    
    def pre_head(self, *args, **kwargs):
        pass
    
    def post_head(self, head, *args, **kwargs):
        pass
    
    def pre_render(self, *args, **kwargs):
        pass
    
    def post_render(self, html, *args, **kwargs):
        pass

def test_plugin_create():
    """Test if plugin is created"""
    plugin = ExamplePlugin()
    assert plugin is not None
    assert isinstance(plugin, ExamplePlugin)
    assert isinstance(plugin, PluginBase)
    assert isinstance(plugin, ABC)

def test_plugin_create_with_parameters():
    """Test if plugin is created with parameters"""
    plugin = ExamplePluginWithParams("foo", bar="bar")
    assert hasattr(plugin, "foo")
    assert plugin.foo == "foo"
    assert hasattr(plugin, "bar")
    assert plugin.bar == "bar"

def test_plugin_raise_notimplementederror():
    """Test if plugin raises NotImplementedError"""
    plugin = ExamplePlugin()
    with pytest.raises(NotImplementedError):
        plugin.pre_data()
    
    with pytest.raises(NotImplementedError):
        plugin.post_data(None)
    
    with pytest.raises(NotImplementedError):
        plugin.pre_head()
    
    with pytest.raises(NotImplementedError):
        plugin.post_head(None)
    
    with pytest.raises(NotImplementedError):
        plugin.pre_render()
    
    with pytest.raises(NotImplementedError):
        plugin.post_render(None)

def test_plugin_methods():
    """Test if plugin methods are called"""
    plugin = ExamplePluginWithAllMethods()
    plugin.pre_data()
    plugin.post_data(None)
    plugin.pre_head()
    plugin.post_head(None)
    plugin.pre_render()
    plugin.post_render(None)
