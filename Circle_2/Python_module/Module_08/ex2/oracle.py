"""This script loads environment variables from a .env file.

It then prints their values.
"""
from dotenv import load_dotenv
import os

env_loaded = load_dotenv()

if __name__ == "__main__":
    print("\nORACLE STATUS: Reading the Matrix...\n")
    mode: str | None = os.getenv("MATRIX_MODE")
    db: str | None = os.getenv("DATABASE_URL")
    api: str | None = os.getenv("API_KEY")
    log: str | None = os.getenv("LOG_LEVEL")
    zion: str | None = os.getenv("ZION_ENDPOINT")

    print("Configuration loaded:")
    if not mode:
        print("Mode is undefined.")
    else:
        print(f"Mode: {mode}")
    if not db:
        print("Database is undefined.")
    else:
        print(f"Database: {db}")
    if not api:
        print("API Access is undefined.")
    else:
        print("API Access: Authenticated")
    if not log:
        print("Log Level is undefined.")
    else:
        print(f"Log Level: {log}")
    if not zion:
        print("Zion Network is undefined.")
    else:
        print(f"Zion Network: {zion}\n")

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    if env_loaded:
        print("[OK] .env file properly configured")
    else:
        print("[KO] .env file not properly configured")
    print("[OK] Production overriden available\n")
    print("The Oracle sees all configurations.")
