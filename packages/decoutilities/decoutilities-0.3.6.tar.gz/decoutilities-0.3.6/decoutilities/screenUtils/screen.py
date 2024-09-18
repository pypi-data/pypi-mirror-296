import os

class Screen:
    def __init__(self):
        self.width, self.height = self.get_terminal_size()

    def get_terminal_size(self):
        size = os.get_terminal_size()
        return size.columns, size.lines

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getCenter(self):
        center_x = self.width // 2
        center_y = self.height // 2
        return center_x, center_y
        
    def freeze(self, allowEscape=True, timeout=-1, message="Terminal paused, new input will not be accepted. Press any key to continue..."):
        import msvcrt
        import time
        timeoutmsg = None
        last_printed_second = None
        if timeout > 0:
            start_time = time.time()
            timeoutmsg = message
        else:
            print(message)
        while True:
            current_time = time.time()
            if timeout > 0 and current_time - start_time > timeout:
                return
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'\x1b' and not allowEscape:
                    continue
                return
            if timeoutmsg:
                current_second = int(current_time)
                if last_printed_second != current_second:
                    remaining_time = timeout - (current_time - start_time)
                    print(timeoutmsg.format(time=round(remaining_time)), end='\r')
                    last_printed_second = current_second