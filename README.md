# Trading Psychology and Evaluation Program
## Overview
This Python-based command-line application helps traders evaluate their psychological readiness and make informed trading decisions. The program offers various utilities, such as a psychology test, trade evaluation based on predefined models, the ability to view available models, and the option to add new evaluation models. All results and models are stored locally, making it easy for users to revisit their evaluations and customize their trading approach.

## Features
### 1. Psychology Test:

 - Purpose: Helps traders assess their psychological readiness before starting a trading session. The test includes several questions about mental and physical preparedness.

- How It Works: After answering a set of yes/no questions, the program calculates the total score, percentage, and provides feedback on whether the trader is ready to trade.
- Result Storage: The test results are saved in a Results directory (created if it doesn't exist) with details like name, score, and date.

### 2. Trade Evaluation:

- Purpose: Assesses the suitability of an asset for trading based on a predefined evaluation model. These models contain questions with assigned points to evaluate market conditions.
- How It Works: Users select an asset model from the Models directory, answer yes/no questions, and the program calculates a final score based on their answers. If the score exceeds 70%, the trader is advised to trade the asset.
- Result Storage: The results are saved in the Results directory under a timestamped file, with details such as the asset name, user’s score, and status.

### 3. Show Models:

- Purpose: Displays all available trading evaluation models stored in the Models directory. These models are text files with predefined questions and points.
- How It Works: Lists all models in a numbered format, allowing users to view which models are available for trade evaluation.

### 4. Add Models:

- Purpose: Allows users to create and add new trading evaluation models. These models can then be used in the Trade Evaluation feature.
- How It Works: Users specify how many questions they want to add, input the questions and their corresponding points, and the model is saved in the Models directory for future evaluations.

### 5. Directory Structure

The program uses two directories for storing results and models:

#### Models/:

Stores the evaluation models, which are plain text files containing questions and associated points.
Models can be created using the "Add Models" option in the program.

#### Results/:

Stores all evaluation and psychology test results in timestamped text files.
Files are saved automatically after each evaluation or psychology test.
##
### Usage
#### Menu Options
#### Psychology Test:

Take a series of yes/no questions to assess your readiness to trade.
Example questions: "Did I wake up feeling rested?", "Is my trading environment distraction-free?"
Trade Evaluation:

Select a model from the available list and evaluate an asset based on predefined market conditions.
You will provide inputs like asset name and time frame (e.g., Weekly, Daily).
Show Models:

View all available models stored in the Models directory. Models contain questions used in the trade evaluation.
Add Models:

Create new evaluation models by specifying a set of questions and assigning points to each question.
Exit:

Exit the program.

## Installation and Running the Program

### 1. Clone the Repository:
git clone https://github.com/username/trading-evaluation.git
cd trading-evaluation

### 2. Run the Program:
python3 program.py

### 3. Dependencies:
- Ensure you have Python 3.x installed.
- No additional dependencies are required for this program.

##


### Contribution
Feel free to fork the repository and create a pull request if you wish to contribute to the project. Issues and suggestions are also welcome.

### License
This project is licensed under the MIT License. See the LICENSE file for details.
##
### Author
Projjal K Roy
GitHub: https://github.com/projjalroy
Email: projjal_r@hotmail.com
##
