# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    myprompt.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbernand <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/16 10:02:52 by rbernand          #+#    #+#              #
#    Updated: 2015/08/23 18:37:29 by rbernand         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import readline

class Completer:
    def __init__(self, words):
        self._words = words
        self._prefix = None

    def complete(self, prefix, index):
        if prefix != self._prefix:
            matching_words = [w for w in self._words if w.startswith(prefix)]
            self._prefix = prefix
        try:
            return matching_words[index]
        except IndexError:
            return None

class Command:
    def __init__(self, name, action, helper, nbargs, transform):
        self._name = name
        self._action = action
        self._helper = helper
        self._nbargs = nbargs
        self._trans = transform

    def _transform(self, args):
        new_args = []
        for trans, arg in zip(self._trans, args):
            new_args.append(trans(arg))
        if len(args) != len(new_args):
            new_args += list(args[len(new_args):])
        return new_args

    def getName(self):
        return self._name

    def getHelper(self):
        return self._helper

    def setAction(self, action):
        self._action = action

    def execute(self, *args, **kwargs):
        if self._nbargs and len(args) != self._nbargs:
            print("Invalid number of argument. %d are required" % self._nbargs)
        elif self._action:
            try:
                self._action(*self._transform(args), **kwargs)
            except ValueError:
                print("Argument invalid.")
            except TypeError:
                print("Too many arguments.")
        else:
            print("Undefined Behaviour.")

    def str_verbose(self):
        return "%s (%s) : %s" % (
                self._name,
                ",".join([str(t.__name__) for t in self._trans]),
                self._helper)

class myPrompt:
    def __init__(self, text="$>"):
        self._commands = [Command("help", self._print_usage, "Display this message.", 0, [])]
        self._text = text
        self._completer = None

    def _getCommand(self, command):
        for cmd in self._commands:
            if cmd.getName() == command:
                return cmd
        return None

    def _print_usage(self):
        for cmd in self._commands:
            print("\t" + cmd.str_verbose())

    def start(self):
        completer = Completer(self._getCommandsList())
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)
        while True:
            line = input(self._text)
            line = line.split()
            if len(line) == 0:
                continue
            cmd = self._getCommand(line[0])
            if cmd:
                cmd.execute(*line[1:])
            else:
                print("Unknow command: %s"  % line[0])
                self._print_usage()

    def _isCommand(self, command):
        for cmd in self._commands:
            if cmd.getName() == command:
                return cmd
        return None

    def _getCommandsList(self):
        keywords = []
        for cmd in self._commands:
            keywords.append(cmd.getName())
        return keywords

    def addCommand(self, name, action=None, helper="Help not defined.", nbargs=None, transform=[]):
        """
            action: function called when command is enter
            helper: text message displayed for help usage
            nbargs: nb of required arguments
            transform: list of constructor for the arguements ti change their type (default is str)
        """
        self._commands.append(Command(name, action, helper, nbargs, transform))
