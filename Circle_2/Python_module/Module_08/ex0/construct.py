"""Checks if the user is in a virtual environment."""
import sys
import os


if __name__ == "__main__":
    in_venv: bool = sys.prefix != sys.base_prefix
    if in_venv:
        print("\nMATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}\n")
        print("SUCCESS: You're in an isolated environment!")
        print(
            "Safe to install packages without affecting the global system.\n"
        )
        print("Package installation path:")
        for path in sys.path:
            if path.endswith("site-packages"):
                print(path)
    else:
        print("\nMATRIX STATUS: You're still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate   # On Unix\n")
        print("matrix_env")
        print("Scripts")
        print("activate     # On Windows\n")
        print("Then run this program again.")
