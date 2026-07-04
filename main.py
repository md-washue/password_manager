import argparse
import getpass
from database import init_db, get_salt, save_password, retrieve_password
from crypto import derive_key, encrypt_data, decrypt_data
from generator import generate_strong_password

def main():
    # Ensure the database and tables exist before doing anything
    init_db()
    
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Secure Command-Line Password Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Command: Add a password
    add_parser = subparsers.add_parser("add", help="Add a new password to the vault")
    add_parser.add_argument("service", help="Name of the service (e.g., github)")
    add_parser.add_argument("username", help="Your username for the service")

    # Command: Get a password
    get_parser = subparsers.add_parser("get", help="Retrieve a password from the vault")
    get_parser.add_argument("service", help="Name of the service to retrieve")

    # Command: Generate a password
    gen_parser = subparsers.add_parser("generate", help="Generate a secure password")
    gen_parser.add_argument("--length", type=int, default=16, help="Length of the password (default 16)")

    args = parser.parse_args()

    # Handle the 'generate' command
    if args.command == "generate":
        print(f"Generated Password: {generate_strong_password(args.length)}")
        return

    # Handle the 'add' and 'get' commands (both require the master password)
    if args.command in ["add", "get"]:
        # getpass hides the typing in the terminal so no one looking over your shoulder sees it
        master_pw = getpass.getpass("Enter Master Password: ")
        
        # Reconstruct the encryption key
        salt = get_salt()
        key = derive_key(master_pw, salt)

        if args.command == "add":
            target_pw = getpass.getpass(f"Enter password for {args.service}: ")
            encrypted_pw = encrypt_data(key, target_pw)
            save_password(args.service, args.username, encrypted_pw)
            print(f"[*] Successfully secured and saved credentials for {args.service}.")

        elif args.command == "get":
            result = retrieve_password(args.service)
            if result:
                username, encrypted_pw = result
                try:
                    decrypted_pw = decrypt_data(key, encrypted_pw)
                    print("\n--- Credentials Found ---")
                    print(f"Service:  {args.service}")
                    print(f"Username: {username}")
                    print(f"Password: {decrypted_pw}")
                    print("-------------------------\n")
                except Exception:
                    # If AES-GCM tag verification fails (wrong password or tampered DB)
                    print("[!] Error: Invalid Master Password or Corrupted Data.")
            else:
                print(f"[!] No credentials found for {args.service}.")

    elif args.command is None:
        parser.print_help()

if __name__ == "__main__":
    main()
