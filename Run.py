#!/usr/bin/env python3
import os
import uuid
import datetime
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
    # Save the license file in the same directory where the script is running
    current_directory = os.path.dirname(os.path.abspath(__file__))
    license_path = os.path.join(current_directory, file_name)
    
    with open(license_path, 'wb') as f:
        f.write(license_key)

# Function to load the license from the file in the current directory
def load_license(file_name='license.key'):
    # Load the license file from the same directory where the script is running
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
    
    # Ensure the Results directory exists
    ensure_directory(results_dir)

    # Ensure the Archive directory exists
    ensure_directory(archive_dir)

    # Get the current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Check all files in the Results directory
    for file_name in os.listdir(results_dir):
        file_path = os.path.join(results_dir, file_name)
        
        # Skip directories, we are only interested in files
        if os.path.isfile(file_path):
            # Extract the date part from the filename (assuming it contains the date)
            if current_date not in file_name:
                # Move old files to the Archive folder
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
    
    # Ask each question and validate input
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
    
    # Calculate percentage score
    percentage_score = (score / total_questions) * 100
    print(f"\nYour total score is: {score}/{total_questions} ({percentage_score:.2f}%)")

    # Decide if the user should trade today
    if percentage_score >= 70:
        trading_status = "You can trade today."
    else:
        trading_status = "Don't trade today."
    print(trading_status)

    # Collect user information
    user_name = input("\nEnter your name: ").strip()
    trading_type = input("Enter your type of trading (e.g., Systematic, Discretionary): ").strip()

    # Save the result to a text file in the Results directory
    save_result(user_name, trading_type, score, total_questions, percentage_score, trading_status)

    # Thank you note
    print("\nThank you for using the Trading Psychology Evaluation Program!")

    # Wait for the user to exit
    input("Press 'Enter' to return to the main menu...")

# Save the result of the psychology test to the Results directory
def save_result(name, trading_type, score, total_questions, percentage_score, trading_status):
    # Ensure the Results directory exists
    results_dir = os.path.join(os.getcwd(), "Results")
    ensure_directory(results_dir)
    
    # Get the current date in YYYY-MM-DD format for the filename
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Filepath to save the result in the Results directory
    file_name = f"Psychology-Test_{date_str}.txt"
    file_path = os.path.join(results_dir, file_name)

    # Get the current date and time for the content of the file
    date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the result content
    result = f"Date/Time: {date_time_str}\nName: {name}\nType of Trading: {trading_type}\n" \
             f"Score: {score}/{total_questions} ({percentage_score:.2f}%)\nStatus: {trading_status}\n\n"
    
    # Write the result to the file (append mode)
    with open(file_path, 'a') as file:
        file.write(result)

    print(f"\nResult saved to: {file_path}")
# Option 2: Trade Evaluation
def trade_evaluation():
    print("\n" + "*" * 50)
    print(" " * 10 + "Trade Evaluation")
    print("*" * 50)

    # Ensure Models directory exists
    models_dir = os.path.join(os.getcwd(), "Models")
    ensure_directory(models_dir)

    # Get the list of files in the Models directory
    model_files = [f for f in os.listdir(models_dir) if os.path.isfile(os.path.join(models_dir, f))]
    
    if not model_files:
        print("No models available in the Models directory.")
        input("Press 'Enter' to return to the main menu...")
        return

    # Display available models
    print("\nAvailable Models for Evaluation:")
    for i, file in enumerate(model_files, 1):
        print(f"{i}. {file}")

    # Ask user to choose a model by number
    while True:
        try:
            model_choice = int(input("\nWhich model do you want to evaluate? (Enter the number): "))
            if 1 <= model_choice <= len(model_files):
                selected_model = model_files[model_choice - 1]
                break
            else:
                print(f"Please enter a valid number between 1 and {len(model_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Collect general information
    user_name = input("\nYour Name: ").strip()
    asset_name = input("Name of the Asset (e.g., ETHUSD/EURUSD): ").strip()
    time_frame = input("Higher Time Frame Chart (Weekly/Daily/Monthly): ").strip()

    # Read the selected model file
    model_path = os.path.join(models_dir, selected_model)
    with open(model_path, 'r') as file:
        questions_data = file.readlines()

    total_points = 0
    user_score = 0
    no_answers = []

    # Ask each question from the model
    print("\nPlease answer the following questions (yes/no):")
    for i, line in enumerate(questions_data):
        question, points = line.strip().split('|')
        points = int(points)
        while True:
            answer = input(f"{question.strip()} (yes/no): ").strip().lower()
            if answer == 'yes':
                user_score += points
                break
            elif answer == 'no':
                no_answers.append(question.strip())
                break
            else:
                print("Invalid input. Please answer 'yes' or 'no'.")
        total_points += points

    # Calculate percentage
    percentage = (user_score / total_points) * 100
    status = "You can trade this asset today" if percentage >= 70 else "Don't trade this asset, find something else"
    
    # Display results
    print(f"\nTotal Points: {user_score}/{total_points}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Status: {status}")

    # Save results to file in the Results directory
    results_dir = os.path.join(os.getcwd(), "Results")
    ensure_directory(results_dir)

    result_file_name = f"Trade-Evaluation_{datetime.now().strftime('%Y-%m-%d')}.txt"
    result_file_path = os.path.join(results_dir, result_file_name)

    with open(result_file_path, 'a') as result_file:
        result_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d')}\n")
        result_file.write(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")
        result_file.write(f"User Name: {user_name}\n")
        result_file.write(f"Asset Name: {asset_name}\n")
        result_file.write(f"Higher Time Frame: {time_frame}\n")
        result_file.write(f"Model Name: {selected_model}\n")
        result_file.write(f"Score: {user_score}/{total_points}\n")
        result_file.write(f"Percentage: {percentage:.2f}%\n")
        result_file.write(f"Status: {status}\n")
        if no_answers:
            result_file.write("Questions answered 'No':\n")
            for no_answer in no_answers:
                result_file.write(f"- {no_answer}\n")
        result_file.write("\n--------------------------------------\n\n")

    print(f"\nResults saved to: {result_file_path}")
    input("Press 'Enter' to return to the main menu...")

# Option 3: Bias Identification
def print_bias_identification_heading():
    print("\n" + "*" * 50)
    print(" " * 10 + "Trading Bias Evaluation")
    print("*" * 50)
    print("Answer the questions honestly to evaluate your bias based on ERL>IRL for trading today.")
    print("Ensure you're in the right bias for your asset before you trade.\n")

def bias_identification():
    questions = [
        "Does the market tagging the HTF ERL/IRL (e.g.,Daily/Weekly/Monthl)?",
        "Is there SMT formation with a correlated pair in the HTF POI?",
        "Has the market retested the POI situated OTE levels on the HTF Swing points? (e.g., 0.5% to 0.786% Fibonacci range)?",
        "Does there any Clear DOL on the opposite side above or bellow Fib 50%",
        "Do we have any Clear MSS with aligned TF ? After the HTF Liq grab?",
        "Was SH or STL taken on MTF before MSS confirmation?",
        "Is there MTF clear POI after the MTF-MSS confirmation? (e.g., OB,FVG,Breaker)",
        "Is there any red folder news events ahead days?",
        "Does the market align with the HTF QT Bias?",
    ]
    
    score = 0
    total_questions = len(questions)
    
    # Ask each question and validate input
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
    
    # Calculate percentage score
    percentage_score = (score / total_questions) * 100
    print(f"\nYour total score is: {score}/{total_questions} ({percentage_score:.2f}%)")

    # Decide if the user should trade today
    if percentage_score >= 70:
        trading_status = "Your bias is good, trade this asset on LTF."
    else:
        trading_status = "Bias isn't strong enough. Don't trade this asset."
    print(trading_status)

    # Collect user information
    asset_name = input("\nEnter the asset name: ").strip()
    chart_timeframe = input("Enter the chart time frame: ").strip()
    trading_type = input("Enter your Bias (e.g., Bullish/Bearish): ").strip()
    
    # Collect image paths for HTF, MTF, LTF
    image_paths = {
        "HTF": input("Enter the path to the HTF image (or press Enter to skip): ").strip(),
        "MTF": input("Enter the path to the MTF image (or press Enter to skip): ").strip(),
        "LTF": input("Enter the path to the LTF image (or press Enter to skip): ").strip()
    }
    
    # Save results and images
    save_bias_result(asset_name, trading_type, chart_timeframe, score, total_questions, percentage_score, trading_status, image_paths)

    # Thank you note
    print("\nThank you for using the Trading Bias Evaluation Program!")
    input("Press 'Enter' to return to the main menu...")

# Save the result of the Bias Evaluation to the Results directory
def save_bias_result(asset_name, trading_type, chart_timeframe, score, total_questions, percentage_score, trading_status, image_paths):
    # Ensure the Results directory exists
    results_dir = os.path.join(os.getcwd(), "Results")
    ensure_directory(results_dir)
    
    # Ensure the Chat_image directory exists
    images_dir = os.path.join(os.getcwd(), "Chat_image")
    ensure_directory(images_dir)

    # Save images to the Chat_image directory
    image_references = []
    for key, path in image_paths.items():
        if os.path.exists(path):
            image_file_name = f"{key}_{asset_name}_Image_{datetime.now().strftime('%Y-%m-%d')}.png"
            image_file_path = os.path.join(images_dir, image_file_name)
            shutil.copy(path, image_file_path)
            image_references.append(f"{key} Image: {image_file_path}")
        else:
            image_references.append(f"{key} Image: Not provided")

    # Save text result in the Results directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    text_file_name = f"Bias_Evaluation_{date_str}.txt"
    text_file_path = os.path.join(results_dir, text_file_name)

    date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = (f"Date/Time: {date_time_str}\nName: {asset_name}\nType of Bias: {trading_type}\n"
              f"Chart Time Frame: {chart_timeframe}\nScore: {score}/{total_questions} ({percentage_score:.2f}%)\n"
              f"Status: {trading_status}\n" + "\n".join(image_references) + "\n\n")
    
    with open(text_file_path, 'a') as file:
        file.write(result)

    print(f"\nResult saved to: {text_file_path}")
    print(f"Images (if any) saved to: {images_dir}")

# Option 4: Show Models
def show_models():
    print("\n" + "*" * 50)
    print(" " * 10 + "Show Models")
    print("*" * 50)

    # Ensure Models directory exists
    models_dir = os.path.join(os.getcwd(), "Models")
    ensure_directory(models_dir)

    # Get the list of files in the Models directory
    model_files = [f for f in os.listdir(models_dir) if os.path.isfile(os.path.join(models_dir, f))]

    if not model_files:
        print("No models available in the Models directory.")
    else:
        print("\nAvailable Models:")
        for i, file in enumerate(model_files, 1):
            print(f"{i}. {file}")

    input("Press 'Enter' to return to the main menu...")

# Option 5: Add Models
def add_models():
    print("\n" + "*" * 50)
    print(" " * 10 + "Add Models")
    print("*" * 50)

    # Ask user for the number of questions
    while True:
        try:
            num_questions = int(input("How many questions do you want to add? "))
            if num_questions <= 0:
                print("Please enter a positive number.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Collect questions and points
    questions_data = []
    for i in range(1, num_questions + 1):
        question = input(f"Enter Question {i}: ").strip()
        while True:
            try:
                points = int(input(f"Enter Points for Question {i} (e.g., 1, 2, 3): "))
                if points <= 0:
                    print("Points must be a positive integer.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        questions_data.append((question, points))

    # Ask for the filename
    file_name = input("Enter a name for the file (without extension): ").strip() + ".txt"

    # Ensure the Models directory exists
    models_dir = os.path.join(os.getcwd(), "Models")
    ensure_directory(models_dir)

    # Save the questions to the file
    file_path = os.path.join(models_dir, file_name)
    with open(file_path, "w") as file:
        for question, points in questions_data:
            file.write(f"{question} | {points}\n")

    print(f"\nQuestions saved successfully to: {file_path}")
    input("Press 'Enter' to return to the main menu...")
    
# Main Menu
def main_menu():
    # Archive old files when the program starts
    archive_old_results()

    while True:
        print("\n" + "=" * 50)
        print(" " * 15 + "Welcome to the Program")
        print("=" * 50)
        print("Please select an option:")
        print("1. Psychology Test")
        print("2. Trade Evaluation")
        print("3. Bias Identification")
        print("4. Show Models")
        print("5. Add Models")
        print("6. Exit")
        print("\nFor more information, visit: https://github.com/projjalroy")  # GitHub link added

        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            print_psychology_heading()
            psychology_test()
        elif choice == '2':
            trade_evaluation()
        elif choice == '3':
            print_bias_identification_heading()
            bias_identification()
        elif choice == '4':
            show_models()
        elif choice == '5':
            add_models()
        elif choice == '6':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    # License check before running the main program
    if check_license():
        main_menu()
    else:
        print("Exiting due to invalid or missing license.")
