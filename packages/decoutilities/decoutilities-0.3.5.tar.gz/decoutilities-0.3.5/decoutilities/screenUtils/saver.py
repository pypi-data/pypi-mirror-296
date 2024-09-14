import os
from decoutilities import experimental
class Saver:
    def __init__(self):
        self.data = None

    def __checkOSName(self):
        # returns Linux for Linux, Darwin for MacOS, and Windows for Windows
        return os.name
    
    #copies all terminal printed stuff to data
    @experimental
    def getTerminalOutput(self):
        # Read terminal history & output to data
        match self.__checkOSName():
            case "Windows":
                os.system("doskey /history > temp.txt")
                with open("temp.txt", "r") as file:
                    self.data = file.read()
                os.remove("temp.txt")
            case "Linux", "Darwin":
                os.system("history > temp.txt")
                with open("temp.txt", "r") as file:
                    self.data = file.read()
                os.remove("temp.txt")
            case _:
                print("Unsupported OS: Unable to get terminal output.")
                
        
    #clears the terminal and prints the data
    def printTerminalOutput(self):
        match self.__checkOSName():
            case "Windows":
                os.system("cls")
            case "Linux", "Darwin":
                os.system("clear")
            case _:
                print("Unsupported OS: Unable to clear terminal.")
        print(self.data)