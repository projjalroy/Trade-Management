import os
import uuid
import shutil
from cryptography.fernet import Fernet
from datetime import datetime

# Encryption Key (should be kept secret)
SECRET_KEY = b'JOnz7KsNi4zXQVrgxHE3b5PVSxd9-XWMgZ1a-bK0WC0='  # Replace with your generated key
cipher = Fernet(SECRET_KEY)

# Function to get machine-specific ID (based on MAC address)
def get_machine_id():
    mac = uuid.getnode()  # This returns the MAC address of the machine
    return str(mac)

# Function to validate the license file
def validate_license(license_key):
    try:
        decrypted_data = cipher.decrypt(license_key).decode()
        machine_id_from_license, expiration_date_str, _ = decrypted_data.split('|')
        expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        current_date = datetime.now()

        # Validate if the license is for this machine and is still valid
        if machine_id_from_license == get_machine_id() and current_date <= expiration_date:
            print("License is valid.")
            return True
        else:
            print("License is invalid or expired.")
            return False
    except Exception as e:
        print(f"Error validating license: {e}")
        return False

# Function to save the new license provided by the user in the current directory
def save_license(license_key, file_name='license.key'):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    license_path = os.path.join(current_directory, file_name)
    
    with open(license_path, 'wb') as f:
        f.write(license_key)

# Function to load the license from the file in the current directory
def load_license(file_name='license.key'):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    license_path = os.path.join(current_directory, file_name)

    try:
        with open(license_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None

# License checking before running the program
def check_license():
    license_file = 'license.key'
    print("Checking license...")

    # Load the existing license key
    license_key = load_license(license_file)

    if license_key and validate_license(license_key):
        print("Program running with valid license.")
        return True
    else:
        print("No valid license found or the license has expired.")
        print(f"Your Unique Machine ID is: {get_machine_id()}")
        
        # Ask user to input a new license key
        new_license_key = input("Please enter your new License Key: ").encode()

        # Validate the new license key
        if validate_license(new_license_key):
            save_license(new_license_key, license_file)
            print("New license saved. Program will now run.")
            return True
        else:
            print("Invalid license. Exiting program.")
            return False

# Utility function to create a directory if it doesn't exist
def ensure_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

# Utility function to archive old result files
def archive_old_results():
    results_dir = os.path.join(os.getcwd(), "Results")
    archive_dir = os.path.join(os.getcwd(), "Archive")
    
    ensure_directory(results_dir)
    ensure_directory(archive_dir)

    current_date = datetime.now().strftime("%Y-%m-%d")

    for file_name in os.listdir(results_dir):
        file_path = os.path.join(results_dir, file_name)
        
        if os.path.isfile(file_path):
            if current_date not in file_name:
                shutil.move(file_path, os.path.join(archive_dir, file_name))
                print(f"Archived old file: {file_name}")

# Option 1: Psychology Test
def print_psychology_heading():
    print("\n" + "*" * 50)
    print(" " * 10 + "Trading Psychology Evaluation")
    print("*" * 50)
    print("Answer the questions honestly to evaluate your readiness for trading today.")
    print("Ensure you're in the right mindset and environment before you trade.\n")

def psychology_test():
    questions = [
        "Did I wake up feeling rested?(e.g., Number of Hours Sleep, Quality of Sleep, Place)",
        "Am I feeling Healthy? (e.g., Feeling sick / Normal)",
        "Did I follow my individual Routine ? (e.g., Exercise /Meditation, or thing’s that you do before you trade)",
        "Did I resolve Negative thoughts and / or emotions? (e.g., arguments, general mental stretches, significantly emotional events)",
        "Is my trading environment one that allows me to focus on trade execution? (e.g., Dedicated space office or room for focus)",
        "Are distractions minimized in order to focus or trading ? (e.g., I don’t talk to anyone before an hour prior to trading)",
        "Did I do everything in my power to create an execution plan that I can follow? (e.g., Create a trading plan or model that makes me feel confident)",
        "Am I aware what others traders sentiment of the market are ? (e.g., Market is bullish/ bearish/undecided)",
        "Is the market condition one that allows me to use my preferred strategy? (e.g., Favorite setup that allows me to trade in this market conditions)",
        "Do I have a strategy that I am proficient at that allows me to trade the current market condition? (e.g., Alternate strategies beside my preferred strategy to turn to)"
    ]
    
    score = 0
    total_questions = len(questions)
    
    for question in questions:
        while True:
            answer = input(f"{question} (yes/no): ").strip().lower()
            if answer == 'yes':
                score += 1
                break
            elif answer == 'no':
                break
            else:
                print("Please enter 'yes' or 'no'.")
    
    percentage_score = (score / total_questions) * 100
    print(f"\nYour total score is: {score}/{total_questions} ({percentage_score:.2f}%)")

    trading_status = "You can trade today." if percentage_score >= 70 else "Don't trade today."
    print(trading_status)

    user_name = input("\nEnter your name: ").strip()
    trading_type = input("Enter your type of trading (e.g., Systematic, Discretionary): ").strip()

    save_result(user_name, trading_type, score, total_questions, percentage_score, trading_status)

    print("\nThank you for using the Trading Psychology Evaluation Program!")
    input("Press 'Enter' to return to the main menu...")

# Save the result of the psychology test to the Results directory
def save_result(name, trading_type, score, total_questions, percentage_score, trading_status):
    results_dir = os.path.join(os.getcwd(), "Results")
    ensure_directory(results_dir)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = f"Psychology-Test_{date_str}.txt"
    file_path = os.path.join(results_dir, file_name)

    date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = f"Date/Time: {date_time_str}\nName: {name}\nType of Trading: {trading_type}\n" \
             f"Score: {score}/{total_questions} ({percentage_score:.2f}%)\nStatus: {trading_status}\n\n"
    
    with open(file_path, 'a') as file:
        file.write(result)

    print(f"\nResult saved to: {file_path}")

# Main Menu
def main_menu():
    archive_old_results()

    while True:
        print("\n" + "=" * 50)
        print(" " * 15 + "Welcome to the Program")
        print("=" * 50)
        print("Please select an option:")
        print("1. Psychology Test")
        print("2. Trade Evaluation")
        print("3. Show Models")
        print("4. Add Models")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            print_psychology_heading()
            psychology_test()
        elif choice == '2':
            trade_evaluation()
        elif choice == '3':
            show_models()
        elif choice == '4':
            add_models()
        elif choice == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    if check_license():
        main_menu()
    else:
        print("Exiting due to invalid or missing license.")
