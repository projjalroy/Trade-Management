#!/usr/bin/env python3
import os
from datetime import datetime

# Utility function to create a directory if it doesn't exist
def ensure_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

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
    
    # Get the current date and time
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Get current date in DD_MM_YY format for unique filename
    date_str = now.strftime("%d_%m_%y")
    
    # Filepath to save the result in the Results directory
    file_name = f"Psychology-Test_{date_str}.txt"
    file_path = os.path.join(results_dir, file_name)

    # Format the result
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

# Option 3: Show Models
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

# Option 4: Add Models
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
    main_menu()
