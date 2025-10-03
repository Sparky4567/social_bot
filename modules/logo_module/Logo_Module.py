from pyfiglet import Figlet
from settings.settings import BOT_NAME
class Logo_Module:
    def __init__(self):
        self.name = BOT_NAME

    def print_logo(self):
        f = Figlet(font="slant")
        print(f.renderText("{}".format(self.name)))