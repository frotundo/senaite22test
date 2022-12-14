=============================
plone.recipe.unifiedinstaller
=============================

This recipe is used by the Unified Installer Buildout to do finishing work like
writing the adminPassword.txt and ZEO control scripts.

Please file bugs to https://dev.plone.org/plone/newticket and specify
the component "Installer (Unified)".

Tests for this recipe are in the Unified Installer.

Options
=======

shell-command
    Full pathname to a POSIX-compliant shell. Used in ZEO start, stop, etc. scripts.
    Default: /bin/sh

sudo-command
    Command -- if needed -- to run process as root. Used only in adminPassword.txt.
    Default: ''

zeoserver
    Name of the ZEO server part if any. If missing, the recipe will scan other
    buildout parts for one using plone.recipe.zope2zeoserver and use its name.
    If a zeoserver is specified or found, ZEO start, stop, etc. scripts will
    be written.

clients
    Names of Zope client parts in the buildout. If missing, the recipe will
    scan other buildout parts for one using 
    plone.recipe.plone.recipe.zope2instance and use their names.

primary-port
    Port of the primary client instance. Used in the adminPassword.txt file.
    Default: 8080

user
    User name and password for the initial Zope administrator. Use
    the format "user:password"
    Default: None. Must be specified.



Change Log
==========

5.2b1 (unreleased)

- Big version change to match Plone target.
  [smcmahon]

- Python 3 compatability.
  [smcmahon]

4.3.3 (unreleased)

  - Fix operation when the var directory is stored in a non-default location.
    [adaugherity]

4.3.2

  - Fix bug that caused failure in buildout if clients were directly specified.
    [smcmahon]

4.3.1

  - Fix bug that prevented plonectl from starting in a non-zeo configuration.
    [MatthewWilkes]


4.3

  - Add new options to handle separate daemon and buildout
    users.

  - Check parts list in a way that doesn't force building of
    every part.

  - Remove backward compatability code that created specific
    function scripts for start/stop/status.

4.0rc1

  - Remove documentation for buildout -n. Add sudo to bin/buildout
    for root installs.

  - When stopping a ZEO cluster, stop the server last.

4.0b3

  - Add 'console' command.

  - Add .html readme.

4.0a1

  - Remove automated creation of Plone site.

0.9

  - Revert damaged logo.

0.8

  - Take buildout:parts-directory into account when writing out
    parts/README.txt. Fixes #9242, Thanks, cah190.

  - Call ``command``-script.py with the current sys.executable if it
    exists, as to run it with pythonw.exe during the Plone Windows
    installer's install.

0.7

  - Quote arguments when init'ing plone site in case
    module path has space(s).

0.6

  - Add "plonectl" general-purpose control script.

  - Add facility to install plone_init_content

0.5

  - Check the directory, not the file. The directory may not
    exist.

0.4

  - Have all the cluster scripts check permissions on var
    before proceeding.

0.3

  - Split adminPassword.txt and README.txt files. Enhance README.

  - Add bin/restartclients.sh script to restart clients only.

0.2

  - Refactored templates and bin scripts into separate files.

  - Restored restartcluster.sh (fixes #7692, thanks Graham Perrin).


