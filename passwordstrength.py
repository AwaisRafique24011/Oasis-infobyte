import re

def check_password_strength(password):
    # Initialize strength score
    strength_score = 0

    # Criteria for evaluation
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password)
    lowercase_criteria = re.search(r'[a-z]', password)
    digit_criteria = re.search(r'\d', password)
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

    # Evaluating the criteria
    if length_criteria:
        strength_score += 1
    if uppercase_criteria:
        strength_score += 1
    if lowercase_criteria:
        strength_score += 1
    if digit_criteria:
        strength_score += 1
    if special_char_criteria:
        strength_score += 1

    # Determine the password strength based on the score
    if strength_score == 5:
        strength = "Very Strong"
    elif strength_score == 4:
        strength = "Strong"
    elif strength_score == 3:
        strength = "Moderate"
    elif strength_score == 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    return strength

while True:
   password = input("Enter your password: ")
   strength = check_password_strength(password)
   print(f"Password Strength: {strength}")
   check = input("Check Again ... Y/N  =  ")
   if check == str.lower("n"):
       break
   
print("Thanks for Using ...")
   
