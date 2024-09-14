from .screen import Screen

class Titler():
    def __init__(self, title, dimiss_message="[ Press any key to dismiss ]"):
        self.title = title
        self.dimiss_message = dimiss_message
        self.screen = Screen()
        self.dimensions = self.screenDimensions()
    
    def screenDimensions(self):
        return self.screen.getWidth(), self.screen.getHeight()
    
    def show(self):
        self.fd, self.flags_save, self.attrs_save = self.getTerminalInfo()
        self.clearScreen()
        self.printTitle()
        self.restoreTerminalInfo((self.fd, self.flags_save, self.attrs_save))

    def clearScreen(self):
        import os
        os.system("cls" if os.name == 'nt' else "clear")

    def getTerminalInfo(self):
        import os
        import sys
        if os.name == 'nt':
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            return None, None, None
        else:
            import termios
            import fcntl
            fd = sys.stdin.fileno()
            flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
            attrs_save = termios.tcgetattr(fd)
            return fd, flags_save, attrs_save

    def restoreTerminalInfo(self, info):
        import os
        import sys
        if os.name == 'nt':
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_TEXT)
        else:
            import termios
            import fcntl
            if info is not None:
                fd, flags_save, attrs_save = info
                fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
                termios.tcsetattr(fd, termios.TCSANOW, attrs_save)
            
    def printTitle(self):
        import msvcrt
        center_x, center_y = self.dimensions[0] // 2, self.dimensions[1] // 2
        print("\n" * center_y + " " * (center_x - len(self.title) // 2) + self.title)
        #same logic for dimiss message
        print("\n" * center_y + " " * (center_x - len(self.dimiss_message) // 2) + self.dimiss_message)
        while True:
            if msvcrt.getch():
                self.clearScreen()
                break