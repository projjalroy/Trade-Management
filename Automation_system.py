# Function to handle the next logic when SMT is confirmed
def proceed_with_next_logic():
    print("Proceeding to the next logic...")
    # Placeholder for further logic
    print("Next logic executed successfully.\n")

# Function to suggest checking another asset or waiting
def suggest_checking_other_assets():
    print("No SMT formed with the correlated pair.")
    action = input("Would you like to check another asset or wait for SMT to form? (check/wait): ").strip().lower()
    if action == "check":
        print("Check another asset for SMT formation.")
        # Optionally, restart the SMT check logic or add additional steps
    elif action == "wait":
        print("Wait for SMT to form on the correlated asset.")
    else:
        print("Invalid input. Please respond with 'check' or 'wait'.")

# Function to check for SMT formation
def check_smt(trend, decision_type):
    smt_response = input(
        f"Is there an SMT (Smart Money Trap) formed with the correlated asset on the HTF chart? (yes/no): "
    ).strip().lower()
    if smt_response == "yes":
        print(f"SMT is confirmed on the HTF chart for {trend} {decision_type}.")
        proceed_with_next_logic()
    elif smt_response == "no":
        suggest_checking_other_assets()
    else:
        print("Invalid input. Please respond with 'yes' or 'no'.")

# Function to handle the logic after IRL or ERL is confirmed
def handle_erl_irl_decision(decision_type):
    # Ask if the decision type (ERL/IRL) is bullish or bearish
    trend = input(f"Is the {decision_type} bullish or bearish? (bullish/bearish): ").strip().lower()
    if trend not in ["bullish", "bearish"]:
        print("Invalid input. Please respond with 'bullish' or 'bearish'.")
        return
    print(f"The {decision_type} is determined to be {trend}.\n")
    
    # Step 3: Check for SMT formation
    check_smt(trend, decision_type)

# Function to determine the HTF ERL/IRL conditions
def check_erl_irl():
    # Ask if the market took the HTF ERL
    erl_response = input("Did the market take the HTF ERL? (yes/no): ").strip().lower()
    if erl_response == "yes":
        handle_erl_irl_decision("HTF ERL")
    else:
        # Ask if the market took the HTF IRL
        irl_response = input("Did the market take the HTF IRL? (yes/no): ").strip().lower()
        if irl_response == "yes":
            handle_erl_irl_decision("HTF IRL")
        else:
            print("Neither HTF ERL nor HTF IRL was taken. No further action.")

# Main function to ask for the HTF and proceed with the decision tree
def main():
    print("=== HTF Decision Program ===")
    htf = input("What is the Higher Time Frame (Daily/Monthly/Weekly)? ").strip().capitalize()
    if htf not in ["Daily", "Monthly", "Weekly"]:
        print("Invalid HTF input. Please choose from Daily, Monthly, or Weekly.")
        return
    print(f"You selected HTF: {htf}\n")
    
    # Proceed to check for HTF ERL or IRL
    check_erl_irl()

# Uncomment the line below to run the program
# main()
