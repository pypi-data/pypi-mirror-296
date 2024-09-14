import msvcrt
import threading
from decoutilities.textUtils import format as color
from utils.legacyLoadingStrategy import legacyLoadingStrategy
from utils.modernLoadingStrategy import modernLoadingStrategy
from command import Command

class pseudoTerminal():
    def __init__(self, prefix='{path} > ', disabledCommands=[], startFolder='~'):
        self.commands = {}
        self.history = []
        self.historyIndex = -1
        import os
        if startFolder ==  '~':
            self.path = self.__detectHomeFolder()
            os.chdir(self.path)  # Change the working directory to the home directory
        else:
            self.path = startFolder
            os.chdir(self.path)  # Change the working directory to the specified start folder
        self.prefix = prefix
        self.disabledCommands = disabledCommands
        self.__loadDefaultCommands()

    def __detectHomeFolder(self):
        import os
        return os.path.expanduser( '~' )

    def addCommand(self, command, func):
        if command not in self.disabledCommands:
            self.commands[command] = func
        else:
            self.commands[command] = self.__commandDisabled

    def addModernCommand(self, command):
        if command.name not in self.disabledCommands and isinstance(command, Command):
            self.commands[command.name] = command

            for alias in command.aliases:
                self.commands[alias] = command
        else:
            self.commands[command.name] = self.__commandDisabled

    def display(self):
        def run():
            while True:
                output = self.__get_input()
                command = output.split(sep=' ')[0]
                # substrct until first space (space also substracted)
                args = []
                for arg in output.split(sep=' '):
                    if (arg != command):
                        args.append(arg)
                self.history.append(command)
                self.historyIndex = -1
                if command in self.commands:
                    self.commands[command](args)
                elif command == "exit":
                    break
                else:
                    print(color('{red}Invalid command'))
        threading.Thread(target=run).start()

    def __loadDefaultCommands(self):
        self.addCommand("exit", exit)
        self.addCommand("help", self.__help)
        self.addCommand("history", self.__history)
        self.addCommand("py", self.__pythonRun)
        self.addCommand("cd", self.__pathSwitch)
        self.addCommand("dir", self.__dir)
        self.addCommand("cat", self.__cat)
        self.addCommand("touch", self.__touch)
        self.addCommand("rm", self.__rm)
        self.addCommand("del", self.__rm)
        self.addCommand("mkdir", self.__mkdir)
        self.addCommand("echo", self.__echo)

    def __help(self, args):
        print("Commands:")
        for command in self.commands:
            print(command)

    def __history(self, args):
        for command in self.history:
            print(command)
    def __get_input(self):
        command = ''
        print(color('{blue}' + self.prefix.replace('{path}', self.path)), end='', flush=True)
        while True:
            prefix = self.prefix.replace('{path}', self.path)
            key = msvcrt.getch().decode('utf-8', errors='ignore')
            if key == '\r':  # Enter key pressed
                print()
                break
            elif key == '\b':  # Backspace key pressed
                command = command[:-1]
                print('\r' + color('{blue}' + prefix) + ' ' * (len(prefix) + len(command)) + '\r' + color('{blue}' + prefix + command), end='', flush=True)
                continue
            elif key == '\t':  # Tab key pressed
                matches = [cmd for cmd in self.commands if cmd.startswith(command)]
                if matches:
                    command = matches[0]
                    print('\r' + color('{blue}' + prefix) + ' ' * (len(prefix) + len(command)) + '\r' + color('{blue}' + prefix + command), end='', flush=True)
                continue
            command += key
            print(key, end='', flush=True)
            matches = [cmd for cmd in self.commands if cmd.startswith(command)]
            if matches:
                first_word = command.split(' ')[0]
                if first_word in self.commands:
                    if isinstance(self.commands[first_word], Command):
                        autocomplete_text = self.commands[first_word].onAutoComplete()
                        print('\r' + color('{blue}' + prefix) + color('{green}' + first_word) + color('{white}' + command[len(first_word):]) + color('{dark_gray}' + autocomplete_text), end='', flush=True)
                    else:
                        print('\r' + color('{blue}' + prefix) + color('{green}' + first_word) + color('{white}' + command[len(first_word):]) + color('{dark_gray}' + matches[0][len(command):]), end='', flush=True)
                else:
                    print('\r' + color('{blue}' + prefix) + color('{red}' + first_word) + color('{white}' + command[len(first_word):]) + color('{dark_gray}' + matches[0][len(command):]), end='', flush=True)
                if (command not in self.commands):
                    print("\033[%dD" % len(matches[0][len(command):]), end='', flush=True)  # move cursor back
        return command
        
    def __pythonRun(self, args):
        if args and args[0] != '':
            cmd = args[0]
            try:
                exec(cmd)
                print(color('{green}Ran command: ' + cmd))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            print(color('{red}This command takes at least one argument.'))
    
    def __commandDisabled(self, args):
        print(color('{red}This command is disabled.'))

    def __pathSwitch(self, args):
        import os
        if args and args[0] != '':
            new_path = args[0]
            try:
                os.chdir(new_path)
                self.path = os.getcwd()  # Get the current working directory after changing it
                self.path = self.path.replace(self.__detectHomeFolder(), '~')
                print(color('{green}Directory changed to: ' + self.path + '. Enjoy your stay!'))  # Print the updated path with a custom message
            except FileNotFoundError:
                print(color('{red}Error: Directory not found'))
            except PermissionError:
                print(color('{red}Error: Permission denied'))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            self.path = self.__detectHomeFolder()
            print(color('{green}Directory changed to home. Welcome back!'))  # Print a custom message when changing to the home directory
                        
    def __dir(self, args):
        import os
        directories = []
        files = []
        for item in os.listdir():
            if os.path.isdir(item):
                directories.append(item)
            else:
                files.append(item)

        for item in directories:
            if item.startswith('.'):  # Check if the directory is hidden
                item_color = 'dark_gray'
            else:
                item_color = 'white'
            try:
                os.chdir(item)  # Try to change to the directory
                os.chdir('..')  # Change back to the parent directory
                print(color('{green}| ' + '{' + item_color + '}📁 ' + item))
            except PermissionError:
                print(color('{red}| ' + '{' + item_color + '}📁 ' + item))

        for item in files:
            if item.startswith('.'):  # Check if the file is hidden
                item_color = 'dark_gray'
            else:
                item_color = 'white'
            if not os.access(item, os.R_OK):  # Check for read permission
                print(color('{red}| ' + '{' + item_color + '}📄 ' + item))
            elif not os.access(item, os.W_OK):  # Check for write permission
                print(color('{yellow}| ' + '{' + item_color + '}📄 ' + item))
            else:
                print(color('{green}| ' + '{' + item_color + '}📄 ' + item))

    def __cat(self, args):
        import os
        if args and args[0] != '':
            file = args[0]
            try:
                with open(file, 'r') as f:
                    print(f.read())
            except FileNotFoundError:
                print(color('{red}Error: File not found'))
            except PermissionError:
                print(color('{red}Error: Permission denied'))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            print(color('{red}This command takes at least one argument.'))

    def __touch(self, args):
        import os
        if args and args[0] != '':
            file = args[0]
            try:
                with open(file, 'w') as f:
                    pass
            except PermissionError:
                print(color('{red}Error: Permission denied'))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            print(color('{red}This command takes at least one argument.'))
    
    def __rm(self, args):
        import os
        if args and args[0] != '':
            file = args[0]
            try:
                os.remove(file)
            except FileNotFoundError:
                print(color('{red}Error: File not found'))
            except PermissionError:
                print(color('{red}Error: Permission denied'))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            print(color('{red}This command takes at least one argument.'))

    def __mkdir(self, args):
        import os
        if args and args[0] != '':
            directory = args[0]
            try:
                os.mkdir(directory)
            except FileExistsError:
                print(color('{red}Error: Directory already exists'))
            except PermissionError:
                print(color('{red}Error: Permission denied'))
            except Exception as e:
                print(color('{red}Unexpected error: ' + str(e)))
        else:
            print(color('{red}This command takes at least one argument.'))
    
    def __echo(self, args):
        if args and args[0] != '':
            print(' '.join(args))
        else:
            print(color('{red}This command takes at least one argument.'))

terminal = pseudoTerminal(disabledCommands=['exit'])
terminal.addCommand("test", lambda: print("Test command"))
terminal.display()