import ctypes
import sys


def handle_windows_terminal():
    """
    Handle specific settings for Windows CMD and PowerShell.
    """
    if sys.platform.startswith("win"):
        try:
            kernel32 = ctypes.windll.kernel32
            # Get the handle to the standard output device (console)
            handle = kernel32.GetStdHandle(-11)
            # Get current console mode
            mode = ctypes.c_uint32()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
            mode.value |= 0x0004
            # Set the new console mode
            kernel32.SetConsoleMode(handle, mode)
        except Exception as e:
            print(
                f"Warning: Unable to set Windows console mode. ANSI colors may not work correctly. Error: {e}",
                file=sys.stderr,
            )
