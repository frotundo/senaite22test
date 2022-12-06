import os

DEP_KEY = 'Z3C_AUTOINCLUDE_DEPENDENCIES_DISABLED'
PLUGIN_KEY = 'Z3C_AUTOINCLUDE_PLUGINS_DISABLED'
DEBUG_KEY = 'Z3C_AUTOINCLUDE_DEBUG'


def dependencies_disabled():
    return DEP_KEY in os.environ


def disable_dependencies():
    os.environ[DEP_KEY] = 'True'


def enable_dependencies():
    os.environ.pop(DEP_KEY, None)


def plugins_disabled():
    return PLUGIN_KEY in os.environ


def disable_plugins():
    os.environ[PLUGIN_KEY] = 'True'


def enable_plugins():
    os.environ.pop(PLUGIN_KEY, None)


def debug_enabled():
    return DEBUG_KEY in os.environ


def disable_debug():
    os.environ.pop(DEBUG_KEY, None)


def enable_debug():
    os.environ[DEBUG_KEY] = 'True'
