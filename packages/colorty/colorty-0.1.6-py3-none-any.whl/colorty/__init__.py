from .core import set_color, reset_color, Clt
from .windows import handle_windows_terminal
from .unix import handle_unix_terminal
from .util import check_environment

# Initialize terminal settings
env = check_environment()
if env == "Windows":
    handle_windows_terminal()
elif env == "Unix":
    handle_unix_terminal()

__all__ = ["set_color", "reset_color", "Clt"]
