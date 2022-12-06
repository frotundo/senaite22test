##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""ZODBMountPoint product.
"""
from logging import getLogger
import sys

LOG = getLogger('Products.TemporaryFolder')


def commit(note):
    import transaction
    transaction.get().note(note)
    transaction.commit()

def install_tempfolder_and_sdc(app):
    from App.config import getConfiguration
    from Acquisition import aq_base
    from .MountedObject import manage_addMounts, MountedObject
    from .MountedObject import getConfiguration as getDBTabConfiguration

    dbtab_config = getDBTabConfiguration()

    tf = getattr(app, 'temp_folder', None)

    if getattr(tf, 'meta_type', None) == MountedObject.meta_type:
        # tf is a MountPoint object.  This means that the temp_folder
        # couldn't be mounted properly (the meta_type would have been
        # the meta type of the container class otherwise).  The
        # MountPoint object writes a message to zLOG so we don't
        # need to.
        return

    if tf is None:
        if dbtab_config is None:
            # DefaultConfiguration, do nothing
            return
        mount_paths = [ x[0] for x in dbtab_config.listMountPaths() ]
        if not '/temp_folder' in mount_paths:
            # we won't be able to create the mount point properly
            LOG.error('Could not initialize a Temporary Folder because '
                      'a database was not configured to be mounted at '
                      'the /temp_folder mount point')
            return
        try:
            manage_addMounts(app, ('/temp_folder',))
            commit(u'Added temp_folder')
            tf = app.temp_folder
        except:
            LOG.error('Could not add a /temp_folder mount point due to an '
                      'error.', exc_info=sys.exc_info())
            return

    # Ensure that there is a transient object container in the temp folder
    config = getConfiguration()

    if not hasattr(aq_base(tf), 'session_data'):
        try:
            from Products.Transience.Transience import TransientObjectContainer
        except ImportError:
            return

        addnotify = getattr(config, 'session_add_notify_script_path', None)
        delnotify = getattr(config, 'session_delete_notify_script_path',
                            None)
        default_limit = 1000
        default_period_secs = 20
        default_timeout_mins = 20

        limit = getattr(config, 'maximum_number_of_session_objects',
                        default_limit)
        timeout_spec = getattr(config, 'session_timeout_minutes',
                               default_timeout_mins)
        period_spec = getattr(config, 'session_resolution_seconds',
                              default_period_secs)

        if addnotify and app.unrestrictedTraverse(addnotify, None) is None:
            LOG.warn('failed to use nonexistent "%s" script as '
                     'session-add-notify-script-path' % addnotify)
            addnotify=None

        if delnotify and app.unrestrictedTraverse(delnotify, None) is None:
            LOG.warn('failed to use nonexistent "%s" script as '
                     'session-delete-notify-script-path' % delnotify)
            delnotify=None

        toc = TransientObjectContainer('session_data',
                                       'Session Data Container',
                                       timeout_mins = timeout_spec,
                                       addNotification = addnotify,
                                       delNotification = delnotify,
                                       limit=limit,
                                       period_secs = period_spec)

        tf._setObject('session_data', toc)
        tf_reserved = getattr(tf, '_reserved_names', ())
        if 'session_data' not in tf_reserved:
            tf._reserved_names = tf_reserved + ('session_data',)
        commit(u'Added session_data to temp_folder')
    return tf # return the tempfolder object for test purposes


def initialize(context):
    # Configure and load databases if not already done.
    from . import MountedObject
    context.registerClass(
        MountedObject.MountedObject,
        constructors=(MountedObject.manage_addMountsForm,
                      MountedObject.manage_getMountStatus,
                      MountedObject.manage_addMounts,),
    )
    app = context.getApplication() # new API added after Zope 4.0b4
    if app is not None:
        install_tempfolder_and_sdc(app)
