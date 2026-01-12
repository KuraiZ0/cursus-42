import sys
import os

if __name__ == "__main__":
    print(f"MATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {sys.executable}")
    in_venv: bool = sys.prefix != sys.base_prefix
    if in_venv:
        print("Virtual Environment: Detected")
    else:
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everythings you install.\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate   # On Unix\n")
    print("matrix_env")
    print("Scripts")
    print("activate     # On Windows\n")
    print("Then run this program again.")
