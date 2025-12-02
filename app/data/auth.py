import bcrypt
import os 
import re

USER_DATA_FILE = "users.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def user_exists(username):
    if not os.path.exists("users.txt"):
        return False

    with open("users.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",", 1)
            if len(parts) != 2:
                continue

            existing_username = parts[0]
            if existing_username == username:
                return True

    return False

def register_user(username, password):
    if user_exists(username):
        return False

    hashed_password = hash_password(password)

    with open("users.txt", "a") as file:
        file.write(f"{username},{hashed_password}\n")

    return True

def login_user(username, password):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                line = line.strip()

                stored_username, stored_hash = line.split(",", 1)

                if stored_username == username:
                    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                        print("Password is correct")
                        return True
                    else:
                        print("Password is incorrect")
                        return False

    except FileNotFoundError:
        print("No users found registered")
        return False

    print("Username not found")
    return False


register_user("testuser", "1234")

def validate_username(username):
    if not username:
        return False, "Username cannot be empty."

    if len(username) < 5:
        return False, "Username must be at least 5 characters long."

    if len(username) > 130:
        return False, "Username cannot exceed 130 characters."

    if not re.match(r'^\w+$', username):
        return False, "Username can only contain special characters."

    return True, ""

def validate_password(password):
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.match(r'^\w+$', password):
        return False, "Password can only contain special characters."

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()
            
             # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()

