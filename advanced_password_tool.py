import hashlib
import re
import os
from termcolor import colored

def score_password(password):
    score = 0
    if len(password) >= 8: score += 20
    if re.search(r"\d", password): score += 20
    if re.search(r"[A-Z]", password): score += 20
    if re.search(r"[a-z]", password): score += 20
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 20
    return score

def check_strength(password):
    score = score_password(password)
    print(colored(f"\nPassword Strength Score: {score}/100", "cyan"))

    if score == 100:
        print(colored("✅ Strong Password", "green"))
    else:
        print(colored("❌ Weak Password. Improve by using:", "red"))
        if len(password) < 8: print("- At least 8 characters")
        if not re.search(r"\d", password): print("- Numbers")
        if not re.search(r"[A-Z]", password): print("- Uppercase letters")
        if not re.search(r"[a-z]", password): print("- Lowercase letters")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): print("- Special characters")

def crack_hash(hash_to_crack, wordlist_file, algorithm):
    with open(wordlist_file, "r", errors='ignore') as f:
        for line in f:
            word = line.strip()
            if algorithm.lower() == "sha256":
                word_hash = hashlib.sha256(word.encode()).hexdigest()
            elif algorithm.lower() == "md5":
                word_hash = hashlib.md5(word.encode()).hexdigest()
            elif algorithm.lower() == "sha1":
                word_hash = hashlib.sha1(word.encode()).hexdigest()
            else:
                print("❌ Unsupported hash algorithm.")
                return

            if word_hash == hash_to_crack:
                print(colored(f"\n✅ Password cracked! It is: {word}", "green"))
                with open("cracked_log.txt", "a") as log:
                    log.write(f"{algorithm.upper()} Hash: {hash_to_crack} = {word}\n")
                return
    print(colored("❌ Password not found in wordlist.", "red"))

def generate_hash(password, algorithm):
    if algorithm.lower() == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm.lower() == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm.lower() == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    else:
        return "Unsupported algorithm."

# Main menu
while True:
    print(colored("\n==== Password Tool Menu ====", "yellow"))
    print("1. Check password strength")
    print("2. Crack hashed password")
    print("3. Generate hash of a password")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":
        pwd = input("🔐 Enter password: ")
        check_strength(pwd)

    elif choice == "2":
        target_hash = input("🔑 Enter hash to crack: ")
        algo = input("💻 Algorithm (sha256/md5/sha1): ")
        wordlist = input("📁 Path to wordlist (e.g., /usr/share/wordlists/rockyou.txt): ")
        if os.path.exists(wordlist):
            crack_hash(target_hash, wordlist, algo)
        else:
            print(colored("❌ Wordlist not found!", "red"))

    elif choice == "3":
        pwd = input("🔐 Enter password: ")
        algo = input("💻 Algorithm (sha256/md5/sha1): ")
        hash_value = generate_hash(pwd, algo)
        print(colored(f"Hash ({algo.upper()}): {hash_value}", "cyan"))

    elif choice == "4":
        print(colored("👋 Exiting. Stay secure!", "yellow"))
        break
    else:
        print(colored("❌ Invalid choice. Try again.", "red"))

