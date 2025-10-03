from pyfiglet import Figlet
from settings.settings import BOT_NAME
from settings.settings import SLOGAN
class Logo_Module:
    def __init__(self):
        self.name = BOT_NAME
        self.slogan = SLOGAN

    def print_logo(self):
        f = Figlet(font="slant")
        print(f.renderText("{}".format(self.name)))

    def print_slogan(self):
        sl = Figlet(font="digital")
        print(sl.renderText("{}".format(self.slogan)))