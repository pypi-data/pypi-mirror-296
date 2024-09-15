# Core functionalities like setting colors
from dataclasses import dataclass


@dataclass
class Clt:
    RESET: str = '\033[39m'
    BLACK: str = '\033[30m'
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    BLUE: str = '\033[34m'
    MAGENTA: str = '\033[35m'
    CYAN: str = '\033[36m'
    WHITE: str = '\033[37m'
    LIGHTBLACK_EX: str = '\033[90m'
    LIGHTRED_EX: str = '\033[91m'
    LIGHTGREEN_EX: str = '\033[92m'
    LIGHTYELLOW_EX: str = '\033[93m'
    LIGHTBLUE_EX: str = '\033[94m'
    LIGHTMAGENTA_EX: str = '\033[95m'
    LIGHTCYAN_EX: str = '\033[96m'
    LIGHTWHITE_EX: str = '\033[97m'

@dataclass
class Style:
    RESET_ALL: str = "\033[0m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = "\033[4m"
    BRIGHT: str = "\033[1m"
    DIM: str = "\033[2m"
    NORMAL: str = "\033[22m"
    
    
def set_color(color):
    """
    Set the terminal text color by color name or ANSI code.
    
    ### Example: 
    set_color('green')
    
    set_color(32)
    
    ### Supported colors:
    - BLACK
    - RED
    - GREEN
    - YELLOW
    - BLUE
    - MAGENTA
    - CYAN
    - WHITE
    - LIGHTBLACK_EX
    - LIGHTRED_EX
    - LIGHTGREEN_EX
    - LIGHTYELLOW_EX
    - LIGHTBLUE_EX
    - LIGHTMAGENTA_EX
    - LIGHTCYAN_EX
    - LIGHTWHITE_EX

    Args:
        color (str or int): Color name or ANSI code.

    Raises:
        AttributeError: If the color name is not valid.
        ValueError: If the ANSI code is not a valid integer.
        
          
    """
    try:
        # Check if input is an integer or a string that can be converted to an integer
        if isinstance(color, int) or (isinstance(color, str) and color.isdigit()):
            color_code = f"\033[{int(color)}m"
        else:
            # Access the color code using the dataclass and color name
            color_code = getattr(Clt, color.upper())
        
        print(color_code, end="")
    except AttributeError:
        print(f"Error: '{color}' is not a valid color name.")
    except ValueError:
        print(f"Error: '{color}' must be a valid integer for ANSI codes.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def reset_color():
    """
    Reset the terminal text color to default.
    """
    try:
        print("\033[0m", end="")
    except Exception as e:
        print(f"Error resetting color: {e}")