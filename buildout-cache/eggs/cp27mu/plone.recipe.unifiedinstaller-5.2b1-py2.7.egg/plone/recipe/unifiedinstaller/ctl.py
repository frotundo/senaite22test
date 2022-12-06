#
# A generic control script for Zope
#
# Copyright (c) 2008, Plone Foundation
# Created by Steve McMahon
#

from __future__ import print_function

import sys
import os.path
import time
import subprocess
import plone.recipe.unifiedinstaller

WIN32 = False
if sys.platform[:3].lower() == "win":
    WIN32 = True

# commands that might make sense issued to multiple targets in a ZEO context
SERVER_COMMANDS = ("start", "stop", "status", "restart",)
if WIN32:
    SERVER_COMMANDS = SERVER_COMMANDS + ("install", "remove")
# commands that make sense issued to a single target
CLIENT_COMMANDS = SERVER_COMMANDS + ("fg", "debug", 'run', 'test', 'adduser', 'console')
ALL_COMMANDS = SERVER_COMMANDS + CLIENT_COMMANDS


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Control(object):

    def __init__(self, server=None, clients=[], location=None, bin_directory=None, file_storage=None):
        self.server = server
        self.clients = clients
        self.location = location
        self.bin_directory = bin_directory
        self.file_storage = file_storage
        self.file_storage_dir = os.path.dirname(file_storage)
        self.firstTime = not os.path.exists(self.file_storage)
        self.modulePath = plone.recipe.unifiedinstaller.__path__[0]
        # put initial components and commands into self.commands,
        # the rest into self.arguments
        self.commands = []
        self.arguments = []
        afound = False
        acommands = (self.server, 'server', 'clients') + tuple(self.clients) + ALL_COMMANDS
        for item in sys.argv[1:]:
            if not afound:
                if item in acommands:
                    self.commands.append(item)
                else:
                    afound = True
            if afound:
                self.arguments.append(item)

    def usage(self):
        if self.server:
            print("Plone control utility")
            print("usage: plonectl %s [component]\n" % ' | '.join(SERVER_COMMANDS))
            print("Available components:")
            print("    Server : %s" % self.server)
            print("    Clients: %s" % ' '.join(self.clients))
            print("\nIf no component is specified, command will be applied to all.")
            print('You may also use "clients" to refer to all clients.\n')
            print('Note that "fg" and "console" may be applied to single components only.')
        else:
            print("usage: plonectl %s\n" % ' | '.join(CLIENT_COMMANDS))
        sys.exit(1)

    def runCommand(self, command, arg=''):
        # run a shell command, return error code

        # make sure output is synchronized with prints
        sys.stdout.flush()

        if isinstance(arg, (tuple, list)):
            args = list(arg) + self.arguments
        else:
            args = [arg, ] + self.arguments

        command_script = os.path.join(self.bin_directory,
                                      "%s-script.py" % command)
        if os.path.exists(command_script):
            args = [sys.executable, command_script] + args
        else:
            args = [os.path.join(self.bin_directory, command)] + args

        po = subprocess.Popen(args)
        try:
            po.communicate()
        except KeyboardInterrupt:
            return 1
        return po.returncode


def main(server=None, clients=[], location=None, bin_directory=None, file_storage=None):

    controller = Control(server, clients, location, bin_directory, file_storage)

    if not os.path.exists(controller.file_storage_dir):
        eprint("%s doesn't exist. Run bin/buildout to configure your installation." % controller.file_storage_dir)
        sys.exit(1)

    if not os.access(controller.file_storage_dir, os.W_OK):
        eprint("You lack the rights necessary to run this script; Try sudo %s" % sys.argv[0])
        sys.exit(1)

    if len(controller.commands) == 1:
        command = controller.commands[0].lower()
        if controller.server:
            # we're going to restrict ourselves to the
            # subset of commands that make sense
            # when starting both a server and clients.
            valid_commands = SERVER_COMMANDS
        else:
            valid_commands = CLIENT_COMMANDS
        if command in valid_commands:
            if controller.server and (command != 'stop'):
                sys.stdout.write("%s: " % controller.server)
                returncode = controller.runCommand(controller.server, command)
                if returncode:
                    sys.exit(returncode)
            for component in controller.clients:
                time.sleep(1)
                sys.stdout.write("%s: " % component)
                returncode = controller.runCommand(component, command)
                if returncode:
                    sys.exit(returncode)
            if controller.server and (command == 'stop'):
                sys.stdout.write("%s: " % controller.server)
                returncode = controller.runCommand(controller.server, command)
                if returncode:
                    sys.exit(returncode)
        else:
            print("Invalid command: %s" % command)
            print("Valid commands in this context are: %s\n" % ', '.join(valid_commands))
            controller.usage()
    elif len(controller.commands) == 2:
        command = controller.commands[0].lower()
        target = controller.commands[1].lower()
        if target in CLIENT_COMMANDS:
            # swap target and command
            s = target
            target = command
            command = s
        if command in CLIENT_COMMANDS:
            if target in ('zeoserver', 'zeo', 'server', controller.server) and \
               controller.server and \
               command in SERVER_COMMANDS:
                sys.stdout.write("%s: " % controller.server)
                returncode = controller.runCommand(controller.server, command)
                if returncode:
                    sys.exit(returncode)
            elif target in controller.clients:
                sys.stdout.write("%s: " % target)
                returncode = controller.runCommand(target, command)
                if returncode:
                    sys.exit(returncode)
            elif target == 'clients':
                for component in controller.clients:
                    time.sleep(1)
                    sys.stdout.write("%s: " % component)
                    returncode = controller.runCommand(component, command)
                    if returncode:
                        sys.exit(returncode)
            else:
                print("No such component: %s\n" % target)
                controller.usage()
        else:
            print("Invalid command: %s\n" % command)
            controller.usage()
    else:
        controller.usage()
