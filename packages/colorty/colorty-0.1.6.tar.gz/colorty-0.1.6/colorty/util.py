import sys

def check_environment():
    """
    Check which environment (Windows, Unix-like) is being used.
    """
    try:
        if sys.platform.startswith('win'):
            return 'Windows'
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return 'Unix'
        else:
            return 'Unknown'
    except Exception as e:
        print(f"Error checking environment: {e}")