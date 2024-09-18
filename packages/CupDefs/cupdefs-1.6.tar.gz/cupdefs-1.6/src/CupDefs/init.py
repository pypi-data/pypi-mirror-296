import colorama
import os

from . import utils
from . import vars
from . import vergen


def init(*args: str) -> bool:
    use_color = True

    if 'no_color' in args:
        utils.pwarn = utils.pdone = utils.perror = utils.pinfo = print
        use_color = False
    else:
        colorama.init(autoreset=True)
    if 'no_vergen' not in args:
        vergen.init_vergen()
    if 'no_logo' not in args:
        utils.print_logo(use_color)
    vars.__CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'
    return True
