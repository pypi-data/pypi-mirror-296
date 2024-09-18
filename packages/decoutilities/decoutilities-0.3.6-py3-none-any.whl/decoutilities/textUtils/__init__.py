class textUtils:
    def color(color, text):
        pattern = "" # {0} is the text
        match color:
            case "red":
                pattern = "\033[91m{0}\033[00m"
            case "green":
                pattern = "\033[92m{0}\033[00m"
            case "yellow":
                pattern = "\033[93m{0}\033[00m"
            case "blue":
                pattern = "\033[94m{0}\033[00m"
            case "purple":
                pattern = "\033[95m{0}\033[00m"
            case "cyan":
                pattern = "\033[96m{0}\033[00m"
            case "white":
                pattern = "\033[97m{0}\033[00m"
            case "dark_red":
                pattern = "\033[31m{0}\033[00m"
            case "dark_green":
                pattern = "\033[32m{0}\033[00m"
            case "gold":
                pattern = "\033[33m{0}\033[00m"
            case "gray":
                pattern = "\033[37m{0}\033[00m"
            case "dark_gray":
                pattern = "\033[90m{0}\033[00m"
            case "black":   
                pattern = "\033[30m{0}\033[00m"
            case "reset":
                pattern = "\033[00m{0}\033[00m"
            case _:
                pattern = "{0}"
        return pattern.format(text)
    def decorate(decoration, text):
        match decoration:
            case "bold":
                return "\033[1m" + text + "\033[0m"
            case "underline":
                return "\033[4m" + text + "\033[0m"
            case "italic":
                return "\033[3m" + text + "\033[0m"
            case _:
                return text

    def hexColor(hexColor, text):
        return "\033[38;2;0x" + hexColor + "m" + text + "\033[0m"
        
    def format(text):
        import re
        aliases = {
            "{bold}": "\033[1m",
            "{underline}": "\033[4m",
            "{italic}": "\033[3m",
            "{red}": "\033[91m",
            "{green}": "\033[92m",
            "{yellow}": "\033[93m",
            "{blue}": "\033[94m",
            "{purple}": "\033[95m",
            "{cyan}": "\033[96m",
            "{white}": "\033[97m",
            "{dark_red}": "\033[31m",
            "{dark_green}": "\033[32m",
            "{gold}": "\033[33m",
            "{gray}": "\033[37m",
            "{dark_gray}": "\033[90m",
            "{black}": "\033[30m",
            "{reset}": "\033[0m"
        }

        for key, value in aliases.items():
            text = text.replace(key, value)

        # Hex {#RRGGBB}
        text = re.sub(r'{#([0-9A-Fa-f]{6})}', r'\033[38;2;0x\1m', text)

        return text + "\033[0m"  # reset at the end
def format(text):
    return textUtils.format(text)
def color(color, text):
    return textUtils.color(color, text)
def decorate(decoration, text):
    return textUtils.decorate(decoration, text)

# FORMAT DECORATOR
def formated(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return format(result)
    return wrapper