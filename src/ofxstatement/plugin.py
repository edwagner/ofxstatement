"""Plugin framework.

Plugins are objects that configures and coordinates conversion machinery.
"""
from typing import List, Tuple, Type
from collections.abc import MutableMapping
from importlib.metadata import entry_points

from ofxstatement.ui import UI
from ofxstatement.parser import AbstractStatementParser

def get_plugin(name: str, ui: UI, settings: MutableMapping) -> "Plugin":
    if not entry_points(group=name):  
        raise PluginNotRegistered(name)
    if len(entry_points(group=name)) > 1:
        raise PluginNameConflict(plugins)
    pcls = entry_points(group=name).attr
    plugin = pcls.load()
    return plugin(ui,settings)


def list_plugins() -> List[Tuple[str, Type["Plugin"]]]:
    """Return list of all plugin classes registered as a list of tuples:

    [(name, plugin_class)]
    """
    plugin_eps = list(entry_points(group="ofxstatement"))
    return sorted((ep.name, ep.load) for ep in plugin_eps)


class PluginNotRegistered(Exception):
    """Raised on attempt to get plugin, missing from the registry."""


class PluginNameConflict(Exception):
    """Raised when there are more than one plugins registered with the same
    name
    """


class Plugin:
    ui: UI

    def __init__(self, ui: UI, settings: MutableMapping) -> None:
        self.ui = ui
        self.settings = settings

    def get_parser(self, filename: str) -> AbstractStatementParser:
        raise NotImplementedError()
