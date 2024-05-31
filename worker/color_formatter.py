class ColorFormatter:
    def __init__(self):
        self.red = "\033[1;31m"
        self.green = "\033[1;32m"
        self.blue = "\033[1;34m"
        self.default = "\033[0m"

    def colorize_red(self, text):
        return f"{self.red}{text}{self.default}"

    def colorize_green(self, text):
        return f"{self.green}{text}{self.default}"

    def colorize_blue(self, text):
        return f"{self.blue}{text}{self.default}"


color_f = ColorFormatter()
