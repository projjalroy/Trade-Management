import os
from datetime import datetime

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_user_info():
    """
    Get the user's name and the asset name.
    """
    user_name = input("Enter your name: ").strip()
    asset_name = input("Enter the asset name: ").strip()
    return user_name, asset_name

def ask_liquidity_type():
    """
    Ask the user which type of liquidity has been taken: Internal or External.
    """
    while True:
        print("\nWhich liquidity has been taken?")
        print("1. Internal Liquidity (FVG)")
        print("2. External Liquidity (BSL/SSL)")
        choice = input("Enter 1 or 2: ").strip()
        
        if choice == '1':
            return 'Internal Liquidity'
        elif choice == '2':
            return 'External Liquidity'
        else:
            print("Invalid input. Please enter 1 or 2.")

def ask_internal_liquidity_followup():
    """
    Ask follow-up questions related to Internal Liquidity (Fair Value Gaps).
    """
    while True:
        fvg_type = input("\nIs the Fair Value Gap (FVG) Bullish or Bearish? (Enter 'Bullish' or 'Bearish'): ").strip().lower()
        if fvg_type in ['bullish', 'bearish']:
            return fvg_type.capitalize()
        else:
            print("Invalid input. Please enter 'Bullish' or 'Bearish'.")

def ask_external_liquidity_followup():
    """
    Ask follow-up questions related to External Liquidity (Buy-side or Sell-side Liquidity).
    """
    while True:
        ext_type = input("\nWas the liquidity taken from the Buy-side or Sell-side? (Enter 'BSL' or 'SSL'): ").strip().upper()
        if ext_type in ['BSL', 'SSL']:
            return ext_type
        else:
            print("Invalid input. Please enter 'BSL' or 'SSL'.")

def ask_timeframe():
    """
    Ask the user for the higher timeframe they are analyzing.
    """
    while True:
        print("\nWhich higher timeframe are you analyzing?")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        choice = input("Enter the number corresponding to the timeframe: ").strip()
        
        timeframes = {
            '1': 'Daily',
            '2': 'Weekly',
            '3': 'Monthly'
        }
        
        if choice in timeframes:
            return timeframes[choice]
        else:
            print("Invalid input. Please enter a number between 1 and 3.")

def determine_midterm_timeframe(timeframe):
    """
    Determine the midterm timeframe based on the given higher timeframe.
    """
    midterm_timeframes = {
        'Daily': '1 Hour',
        'Weekly': '4 Hours',
        'Monthly': 'Daily'
    }
    return midterm_timeframes.get(timeframe, 'Unknown')

def ask_smt_confirmation():
    """
    Ask the user if SMT is confirmed.
    """
    while True:
        smt_confirmed = input("\nIs SMT confirmed? (Enter 'Yes' or 'No'): ").strip().lower()
        if smt_confirmed in ['yes', 'no']:
            return smt_confirmed == 'yes'
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

def ask_midterm_cisd():
    """
    Ask the user if CISD is confirmed on the midterm timeframe.
    """
    while True:
        cisd_confirmed = input("\nIs CISD confirmed on the midterm timeframe? (Enter 'Yes' or 'No'): ").strip().lower()
        if cisd_confirmed in ['yes', 'no']:
            return cisd_confirmed == 'yes'
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

def ask_midterm_mss():
    """
    Ask the user if MSS is confirmed on the midterm timeframe.
    """
    while True:
        mss_confirmed = input("\nIs MSS confirmed on the midterm timeframe? (Enter 'Yes' or 'No'): ").strip().lower()
        if mss_confirmed in ['yes', 'no']:
            return mss_confirmed == 'yes'
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

def ask_erl_irl_location():
    """
    Ask the user where the ERL or IRL is situated.
    """
    while True:
        print("\nWhere is the ERL or IRL situated?")
        print("1. Premium Zone")
        print("2. Discount Zone")
        print("3. Cannot Determine")
        choice = input("Enter 1, 2, or 3: ").strip()
        
        if choice == '1':
            return 'Premium Zone'
        elif choice == '2':
            return 'Discount Zone'
        elif choice == '3':
            return 'Cannot Determine'
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

def determine_bias(fvg_type, erl_irl_location, liquidity_type):
    """
    Determine the bias based on the FVG type, ERL/IRL location, and liquidity type.
    """
    if erl_irl_location == 'Cannot Determine':
        if liquidity_type == 'Internal Liquidity':
            if fvg_type == 'Bullish':
                return 'Low Probability Bullish Bias'
            elif fvg_type == 'Bearish':
                return 'Low Probability Bearish Bias'
        elif liquidity_type == 'External Liquidity':
            if fvg_type == 'SSL':
                return 'Low Probability Bullish Bias'
            elif fvg_type == 'BSL':
                return 'Low Probability Bearish Bias'
    
    if liquidity_type == 'Internal Liquidity':
        if fvg_type == 'Bullish' and erl_irl_location == 'Discount Zone':
            return 'Bullish Bias'
        elif fvg_type == 'Bearish' and erl_irl_location == 'Premium Zone':
            return 'Bearish Bias'
    elif liquidity_type == 'External Liquidity':
        if fvg_type == 'SSL' and erl_irl_location == 'Discount Zone':
            return 'Bullish Bias'
        elif fvg_type == 'BSL' and erl_irl_location == 'Premium Zone':
            return 'Bearish Bias'
    return 'No clear bias'

def bias_identification():
    """
    Perform bias identification.
    """
    user_name, asset_name = get_user_info()
    print(f"\nHello, {user_name}! You are analyzing the asset: {asset_name}\n")
    
    liquidity_type = ask_liquidity_type()
    
    if liquidity_type == 'Internal Liquidity':
        followup = ask_internal_liquidity_followup()
    else:
        followup = ask_external_liquidity_followup()
    
    timeframe = ask_timeframe()
    midterm_timeframe = determine_midterm_timeframe(timeframe)
    smt_confirmed = ask_smt_confirmation()
    
    bias_result = ""
    if not smt_confirmed:
        bias_result = "SMT not confirmed. Continuing with the previous bias."
    else:
        if liquidity_type == 'Internal Liquidity':
            cisd_confirmed = ask_midterm_cisd()
            if cisd_confirmed:
                erl_irl_location = ask_erl_irl_location()
                bias_result = determine_bias(followup, erl_irl_location, liquidity_type)
                bias_result = f"Bias: {bias_result}. Confirmed with Internal Liquidity, SMT, and CISD on {midterm_timeframe} timeframe."
            else:
                bias_result = f"CISD not confirmed. Continuing with the previous bias or wait for CISD to form on {midterm_timeframe} timeframe."
        elif liquidity_type == 'External Liquidity':
            mss_confirmed = ask_midterm_mss()
            if mss_confirmed:
                erl_irl_location = ask_erl_irl_location()
                bias_result = determine_bias(followup, erl_irl_location, liquidity_type)
                bias_result = f"Bias: {bias_result}. Confirmed with External Liquidity, SMT, and MSS on {midterm_timeframe} timeframe."
            else:
                bias_result = f"MSS not confirmed. Continuing with the previous bias or wait for MSS to form on {midterm_timeframe} timeframe."
    
    print(bias_result)

if __name__ == "__main__":
    bias_identification()