#!/usr/bin/env python3
from program import Program
from Seeker import Seeker
from myprompt.myprompt import myPrompt
import signal
import sys
import yaml
import argparse

DEFAULT_CONFIG_FILE = ".default_config.yaml"

def loadYaml(input_file=".default_config.yaml"):
    """
    Function that get the Yaml from a stream and feel the program list

    Args:
        param1 (String): Name of the Yaml.
        default valor is .default_config.yaml
    Returns:
        No return
    Raises:
        FileNotFoundError : case of the file is not here or bad name
    """
    try:
        with open(input_file, 'r') as stream:
            data = yaml.load(stream)
            prg_list = [p.getName() for p in Program.PROGRAMS]
            for prg_name, prg_attr in data['programs'].items():
                if prg_name not in prg_list:
                    Program.PROGRAMS.append(Program(prg_name, prg_attr))
                else:
                    prg = [p for p in Program.PROGRAMS if p.getName() == prg_name][0]
                    prg.updateConfig(prg_attr)
            print("File '%s' successfully loaded." % input_file)
    except FileNotFoundError:
        print("File not found '%s'." % input_file)
    except PermissionError:
        print("Permission Denied '%s'." % input_file)
    except yaml.scanner.ScannerError:
        print("Invalid input file '%s'." % input_file)

def listPrg():
    """
    Function that print the list of the programs names actualy launch

    Args:
        No param
    Returns:
        No return
    Raises:
        No raises
    """
    for i, prg in enumerate(Program.PROGRAMS):
        print("\t{}. {}".format(i, prg.getName()))

def printStatus():
    """
    Function that print the list of the programs status actualy launch

    Args:
        No param
    Returns:
        No return
    Raises:
        No raises
    """
    for i, prg in enumerate(Program.PROGRAMS):
        print("\t{}. {:^12} {:^12} {:^12}".format(i, prg.getName(), prg.getPid(), prg.getStatus()))

def show(prg_id=None):
    """
    Function that print the params of the program by id

    Args:
        param1 (int) : id of the program that we search
    Returns:
        No return
    Raises:
        IndexError : if their is no program at the id send
    """
    if not prg_id:
        for prg in Program.PROGRAMS:
            print("\033[4m" + prg.getName() + "\033[0m")
            print(prg.print_params())
    else:
        try:
            print("\033[4m" + Program.PROGRAMS[prg_id].getName() + "\033[0m")
            print(Program.PROGRAMS[prg_id].print_params())
        except IndexError:
            print("Program Id out of range")

def start_watcher(autostart=False):
    """
    Function that start all program for watch

    Args:
        No param
    Returns:
        No return
    Raises:
        No raises
    """
    for prg in Program.PROGRAMS:
        if autostart:
            print(prg.getAutoStart())
            if prg.getAutoStart():
                prg.execute()
        else:
            prg.execute()

    seeker = Seeker()
    seeker.start()

def exitTM():
    for prg in Program.PROGRAMS:
        prg.kill(signal.SIGINT)
    sys.exit(0)

def stop():
    """
    Function that kill all program

    Args:
        No param
    Returns:
        No return
    Raises:
        No raises
    """
    for prg in Program.PROGRAMS:
        prg.kill(signal.SIGQUIT)

def initParser():
    """
    Function that init the parser and call the prompt
    Args:
        No param
    Returns:
        No return
    Raises:
        No raises
    """
    prompt = myPrompt(text="TaskMaster $>")
    prompt.addCommand("exit", action=exitTM, helper="Quit the program.")
    prompt.addCommand("list", action=listPrg, helper="List the current seeked programs.")
    prompt.addCommand("stop", action=stop, helper="Stop all the process.")
    prompt.addCommand("start", action=start_watcher, helper="Run the sekked Programms.")
    prompt.addCommand("status", action=printStatus, nbargs=0, helper="Show current programs status")
    prompt.addCommand("load", action=loadYaml, nbargs=1, transform=[str], \
        helper="Load config file. Default is '.default_config.yaml")
    prompt.addCommand("show", action=show, transform=[int], helper="Print details of a programm")
    return prompt

def main():
    parrgs = argparse.ArgumentParser()
    parrgs.add_argument("-c", "--config_file", default=DEFAULT_CONFIG_FILE, action="store")
    args = parrgs.parse_args()
    prg = initParser()
    loadYaml(args.config_file)
    start_watcher(True) # add argument for first call
    prg.start()

if __name__ == "__main__":
    main()
