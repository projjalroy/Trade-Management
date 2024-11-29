# Function to handle LTF logic placeholder
def handle_ltf_logic():
    print("Proceeding to LTF (Lower Time Frame) logic...")
    # Placeholder for LTF logic
    print("LTF logic will be added later.\n")

# Function to handle MTF checkpoints for SMT confirmation
def handle_mtf_checkpoints():
    print("=== MTF Checkpoints for SMT Confirmation ===")
    
    # Checkpoint 1: Short-term High/Low purge
    st_purge = input("Was a short-term High/Low purged before the SMT formation? (yes/no): ").strip().lower()
    if st_purge != "yes":
        print("Short-term High/Low purge not confirmed. Reassess conditions.")
        return
    
    # Checkpoint 2: CiSD confirmation
    cisd = input("Has CiSD (Change in State of Delivery) been confirmed? (yes/no): ").strip().lower()
    if cisd == "yes":
        print("CiSD confirmed. Proceeding to LTF logic.")
        handle_ltf_logic()
        return  # Exit here as CiSD confirmation is sufficient
    
    # Checkpoint 3: Breaker Block or MSS formation
    breaker_or_mss = input("Is there any Breaker Block or MSS (Market Structure Shift) formed? (yes/no): ").strip().lower()
    if breaker_or_mss == "yes":
        print("Breaker Block or MSS confirmed. Proceeding to LTF logic.")
        handle_ltf_logic()
    else:
        print("Neither CiSD nor Breaker Block/MSS confirmed.")
        suggest_checking_other_assets()

# Function to suggest checking another asset or waiting
def suggest_checking_other_assets():
    action = input("Would you like to check another asset or wait for this logic to confirm? (check/wait): ").strip().lower()
    if action == "check":
        print("Check another asset for SMT formation.")
    elif action == "wait":
        print("Wait for the current logic to confirm.")
    else:
        print("Invalid input. Please respond with 'check' or 'wait'.")

# Function to handle the next logic when SMT is confirmed
def proceed_with_next_logic():
    print("SMT confirmed on HTF chart with correlated asset.")
    print("Please proceed to MTF (Mid Time Frame) checkpoints for SMT confirmation.")
    handle_mtf_checkpoints()

# Function to check for SMT formation
def check_smt(trend, decision_type):
    smt_response = input(
        f"Is there an SMT (Smart Money Trap) formed with the correlated asset on the HTF chart? (yes/no): "
    ).strip().lower()
    if smt_response == "yes":
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
