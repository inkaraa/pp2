import string 

def generate_alphabet_files():
    for letter in string.ascii_uppercase:
        with open(f"{letter}.txt", 'w', encoding='utf-8') as file:
            file.write(f"This is {letter}.txt")

generate_alphabet_files()