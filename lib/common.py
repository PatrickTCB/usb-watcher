import sys
import subprocess
from os.path import exists

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def colourMe(string, colour="default"):
    if colour.lower() == "purple":
        return "{}{}{}".format(bcolors.PURPLE, string, bcolors.ENDC)
    elif colour.lower() == "blue":
        return "{}{}{}".format(bcolors.BLUE, string, bcolors.ENDC)
    elif colour.lower() == "cyan":
        return "{}{}{}".format(bcolors.CYAN, string, bcolors.ENDC)
    elif colour.lower() == "green":
        return "{}{}{}".format(bcolors.GREEN, string, bcolors.ENDC)
    elif colour.lower() == "yellow":
        return "{}{}{}".format(bcolors.YELLOW, string, bcolors.ENDC)
    elif colour.lower() == "RED":
        return "{}{}{}".format(bcolors.RED, string, bcolors.ENDC)
    else:
        return "{}{}{}".format(bcolors.PURPLE, string, bcolors.ENDC)

def fileToString(fileName) :
    fileContents = ""
    with open(fileName, 'r') as myfile:
        fileContents = myfile.read()
    return str(fileContents)

def stringToFile(fileName, contentsRaw):
    contents = str(contentsRaw)
    with open(fileName, "w+") as output_file:
        output_file.write(contents)
        output_file.close()
        
def parseArgs(allArgs):
    adict = {}
    adict["v"] = False
    i = 1
    for arg in allArgs:
        if arg[0] == "-":
            try:
                adict[arg[1:]] = allArgs[i]
            except IndexError:
                adict[arg[1:]] = True
            except Exception as e:
                print("Couldn't parse {}.\n{}", arg, e)
                sys.exit(3)
        i = i + 1
    return adict

def desktopNotify(title, message):
    terminalNotifier_exists = exists("/opt/homebrew/bin/terminal-notifier")
    if terminalNotifier_exists:
        tmCommand = "/opt/homebrew/bin/terminal-notifier -title '{}' -message '{}' -sound default".format(title, message)
        subprocess.run(tmCommand, shell=True)
    else:
        print("terminal-notifier doesn't seem to be installed. Desktop notification not possible")

def bash(command, verbose=False):
    commandList = command.split(" ")
    if verbose:
        print("{}".format(command))
    commandOutputRaw = subprocess.run(commandList, capture_output=True, text=True).stdout
    if verbose:
        print("{}".format(commandOutputRaw))
    return commandOutputRaw