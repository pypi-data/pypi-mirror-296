from decoutilities.textUtils import format as color
from command import Command

class Cd(Command):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.aliases = []

    def onAutoComplete(self, partialCommand):
        return 'test'   

    def onExecute(self, args):
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
                    
                