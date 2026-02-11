# ENHANCEMENT: Visual Password Strength Display
# Author: Oscar Fonseca
# This program includes a visual strength bar feature that displays the password strength as a progress bar (e.g., [████░░░░░░] 4/5).
# This makes it easier for users to quickly understand password strength at a glance, improving the user experience beyond the basic requirements.

# Constants for character types
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",", ".", "<", ">", "?", "/", "\\", "`", "~"]


def word_in_file(word, filename, case_sensitive=False):
    """Check if a word exists in a file."""
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            file_word = line.strip()
            
            if case_sensitive:
                if word == file_word:
                    return True
            else:
                if word.lower() == file_word.lower():
                    return True
    
    return False


def word_has_character(word, character_list):
    """Check if word contains any character from character_list."""
    for character in word:
        if character in character_list:
            return True
    
    return False


def word_complexity(word):
    """Calculate complexity score based on character types."""
    complexity = 0
    
    if word_has_character(word, LOWER):
        complexity += 1
    
    if word_has_character(word, UPPER):
        complexity += 1
    
    if word_has_character(word, DIGITS):
        complexity += 1
    
    if word_has_character(word, SPECIAL):
        complexity += 1
    
    return complexity


def password_strength(password, min_length=10, strong_length=16):
    """Calculate password strength and provide feedback."""
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0
    
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0
    
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1
    
    if len(password) > strong_length:
        print("Password is long, length trumps complexity this is a good password.")
        return 5
    
    complexity = word_complexity(password)
    strength = 1 + complexity
    
    return strength


def display_strength_bar(strength):
    """
    ENHANCEMENT FUNCTION: Display visual password strength bar.
    Shows strength as a visual progress bar for better user experience.
    
    Parameters:
        strength: integer from 0-5 indicating password strength
    Returns:
        string with visual bar representation
    """
    # Create filled portion (█) and empty portion (░)
    filled = "█" * strength
    empty = "░" * (5 - strength)
    
    # Color coding based on strength
    if strength <= 1:
        status = "WEAK"
    elif strength <= 3:
        status = "MEDIUM"
    else:
        status = "STRONG"
    
    return f"[{filled}{empty}] {strength}/5 - {status}"


def main():
    """Main program loop - gets passwords from user and checks them."""
    print("="*50)
    print("Password Strength Checker")
    print("="*50)
    print("Enter 'q' to quit\n")
    
    while True:
        password = input("Enter a password to test: ")
        
        if password == "q" or password == "Q":
            print("\nGoodbye!")
            break
        
        # Calculate strength
        strength = password_strength(password)
        
        # Display results with visual bar (ENHANCEMENT)
        print(f"Password strength: {display_strength_bar(strength)}")
        print()


if __name__ == "__main__":
    main()