import math
import re
import string
import hashlib
import secrets

COMMON_PASSWORDS = {
    "123456", "password", "qwerty", "letmein", "abc123", "12345678", "iloveyou",
    "admin", "welcome", "monkey", "dragon", "football", "baseball", "111111",
    "sunshine", "master", "hello", "freedom", "whatever", "qazwsx", "trustno1"
}

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_charset(password):
    """Detects the character set size used in the password."""
    charset = set()
    if re.search(r"[a-z]", password):
        charset.update(string.ascii_lowercase)
    if re.search(r"[A-Z]", password):
        charset.update(string.ascii_uppercase)
    if re.search(r"[0-9]", password):
        charset.update(string.digits)
    if re.search(r"[{}]".format(re.escape(string.punctuation)), password):
        charset.update(string.punctuation)
    # Add unicode symbols if present
    if re.search(r"[^\w\s]", password):
        charset.update({c for c in password if not c.isalnum() and not c.isspace()})
    return len(charset)

def calculate_entropy(password):
    """Calculates Shannon entropy based on detected charset."""
    charset_size = calculate_charset(password)
    entropy = math.log2(charset_size) * len(password) if charset_size > 0 else 0
    return round(entropy, 2)

def assess_strength(password):
    entropy = calculate_entropy(password)
    issues = []

    # Length checks
    if len(password) < 8:
        issues.append("Too short 🚨")
    elif len(password) < 12:
        issues.append("Short (consider longer) ⚠️")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        issues.append("Common password ⚠️")

    # Repetitive characters
    if re.fullmatch(r"(.)\1+", password):
        issues.append("Repetitive characters 💤")

    # Only digits or only letters
    if re.fullmatch(r"\d+", password):
        issues.append("Only digits 🔢")
    if re.fullmatch(r"[a-zA-Z]+", password):
        issues.append("Only letters 🔡")

    # Sequential characters
    if re.search(r"(?:0123|1234|2345|3456|4567|5678|6789|abcd|bcde|cdef|defg|efgh|fghi|ghij|hijk|ijkl|jklm|klmn|lmno|mnop|nopq|opqr|pqrs|qrst|rstu|stuv|tuvw|uvwx|vwxy|wxyz)", password.lower()):
        issues.append("Sequential characters ➡️")

    # Keyboard patterns
    if re.search(r"(qwerty|asdf|zxcv|poiuy|lkjh|mnbv)", password.lower()):
        issues.append("Keyboard pattern ⌨️")

    # Entropy-based strength
    if entropy >= 60 and not issues:
        strength = "Strong ✅"
    elif entropy >= 40 and len(issues) <= 1:
        strength = "Good 🟢"
    elif entropy >= 30:
        strength = "Medium 🟡"
    else:
        strength = "Weak 🔴"

    return {
        "Password Hash": hash_password(password),
        "Length": len(password),
        "Charset Size": calculate_charset(password),
        "Entropy": entropy,
        "Strength": strength,
        "Issues": issues if issues else ["None 🎉"]
    }

def generate_password(length=16):
    """Generates a strong random password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def analyze_password(password, show_hash=False):
    """Adapter for CLI wiring. Hashes input and output, asks user if they want to see the hash."""
    result = assess_strength(password)
    if show_hash:
        print(f"Password hash: {result['Password Hash']}")
    else:
        print("Password hash is hidden. Set show_hash=True to display.")
    return result

def cli():
    """Simple CLI for password analysis and generation."""
    print("Choose an option:")
    print("1. Analyze a password")
    print("2. Generate a strong password")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        pwd = input("Enter password to analyze: ")
        show = input("Show password hash? (y/n): ").lower() == "y"
        result = analyze_password(pwd, show_hash=show)
        print(result)
    elif choice == "2":
        length = input("Enter desired password length (default 16): ").strip()
        length = int(length) if length.isdigit() and int(length) > 0 else 16
        pwd = generate_password(length)
        print(f"Generated password: {pwd}")
        show = input("Show password hash? (y/n): ").lower() == "y"
        result = analyze_password(pwd, show_hash=show)
        print(result)
    else:
        print("Invalid choice.")

# Uncomment below to enable CLI usage
# if __name__ == "__main__":
#     cli()
