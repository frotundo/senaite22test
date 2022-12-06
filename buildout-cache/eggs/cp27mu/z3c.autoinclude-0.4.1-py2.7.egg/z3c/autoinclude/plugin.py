import logging
import os
from pkg_resources import iter_entry_points
from pkg_resources import resource_filename
from z3c.autoinclude.api import debug_enabled
from z3c.autoinclude.utils import create_report
from z3c.autoinclude.utils import DistributionManager
from z3c.autoinclude.utils import ZCMLInfo


logger = logging.getLogger("z3c.autoinclude")


class PluginFinder(object):
    def __init__(self, platform_dottedname):
        self.dottedname = platform_dottedname

    def includableInfo(self, zcml_to_look_for):
        includable_info = ZCMLInfo(zcml_to_look_for)

        for plugin_distribution in find_plugins(self.dottedname):
            include_finder = DistributionManager(plugin_distribution)
            for plugin_dottedname in include_finder.dottedNames():
                groups = zcml_to_include(plugin_dottedname, zcml_to_look_for)
                for zcml_group in groups:
                    includable_info[zcml_group].append(plugin_dottedname)

        if debug_enabled():
            report = create_report(includable_info)
            if "overrides.zcml" in zcml_to_look_for:
                report.insert(0, "includePluginsOverrides found in zcml of %s." % self.dottedname)
            else:
                report.insert(0, "includePlugins found in zcml of %s." % self.dottedname)
            logger.info("\n".join(report))

        return includable_info


def find_plugins(dotted_name):
    for ep in iter_entry_points('z3c.autoinclude.plugin'):
        if ep.module_name == dotted_name:
            yield ep.dist


def zcml_to_include(dotted_name, zcmlgroups=None):
    if zcmlgroups is None:
        zcmlgroups = ('meta.zcml', 'configure.zcml', 'overrides.zcml')

    includable_info = []

    for zcmlgroup in zcmlgroups:
        filename = resource_filename(dotted_name, zcmlgroup)
        if os.path.isfile(filename):
            includable_info.append(zcmlgroup)
    return includable_info
