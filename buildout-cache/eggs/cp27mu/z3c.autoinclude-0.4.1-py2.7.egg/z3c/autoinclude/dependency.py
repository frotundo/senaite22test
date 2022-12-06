import os
import logging
from zope.dottedname.resolve import resolve
from pkg_resources import resource_exists
from pkg_resources import get_provider
from pkg_resources import get_distribution
from z3c.autoinclude.api import debug_enabled
from z3c.autoinclude.utils import DistributionManager
from z3c.autoinclude.utils import ZCMLInfo
from z3c.autoinclude.utils import create_report


logger = logging.getLogger("z3c.autoinclude")


class DependencyFinder(DistributionManager):
    def includableInfo(self, zcml_to_look_for):
        """Return the packages in the dependencies which are includable.

        zcml_to_look_for - a list of zcml filenames we are looking for

        Returns a dictionary with the include candidates as keys, and lists
        of dotted names of packages that contain the include candidates as
        values.
        """
        result = ZCMLInfo(zcml_to_look_for)
        for req in self.context.requires():
            dist_manager = DistributionManager(get_provider(req))
            for dotted_name in dist_manager.dottedNames():
                try:
                    module = resolve(dotted_name)
                except ImportError as exc:
                    logger.warning(
                        "resolve(%r) raised import error: %s" % (dotted_name, exc)
                    )
                    continue
                module_file = getattr(module, '__file__', None)
                if module_file is None:
                    logger.warning("%r has no __file__ attribute" % dotted_name)
                    continue
                for candidate in zcml_to_look_for:
                    candidate_path = os.path.join(
                        os.path.dirname(module_file), candidate
                    )
                    if os.path.isfile(candidate_path):
                        result[candidate].append(dotted_name)

        if debug_enabled():
            report = create_report(result)
            if "overrides.zcml" in zcml_to_look_for:
                report.insert(0, "includeDependenciesOverrides found in zcml of %s." % self.context.project_name)
            else:
                report.insert(0, "includeDependencies found in zcml of %s." % self.context.project_name)
            logger.info("\n".join(report))

        return result


def package_includes(project_name, zcml_filenames=None):
    """
    Convenience function for finding zcml to load from requirements for
    a given project. Takes a project name. DistributionNotFound errors
    will be raised for uninstalled projects.
    """
    if zcml_filenames is None:
        zcml_filenames = ['meta.zcml', 'configure.zcml', 'overrides.zcml']
    dist = get_distribution(project_name)
    include_finder = DependencyFinder(dist)
    return include_finder.includableInfo(zcml_filenames)
