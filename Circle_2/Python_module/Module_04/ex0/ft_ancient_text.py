def try_to_access():
    """Trying to open a txt file and print error if an error occured."""
    try:
        file = open("ancient_fragment.txt", "r")
        print("Accessing Storage Vault: ancient_fragment.txt")
        print("Connection established...\n")
        print("RECOVERED DATA:")
        content = file.read()
        print(f"{content}")
        # file.close()
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")


if __name__ == "__main__":
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===")
    print()
    try_to_access()
