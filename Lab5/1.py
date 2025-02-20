import re

def match_a_followed_by_b(string): # 1
    return bool(re.fullmatch(r'a*b*', string))

def match_a_followed_by_two_to_three_b(string): # 2
    return bool(re.fullmatch(r'ab{2,3}', string))

def find_sequences_with_underscore(string): # 3
    return re.findall(r'\b[a-z]+_[a-z]+\b', string)

def find_uppercase_followed_by_lowercase(string): # 4
    return re.findall(r'[A-Z][a-z]+', string)

def match_a_followed_by_anything_ending_in_b(string): # 5
    return bool(re.fullmatch(r'a.*b', string))

def replace_space_comma_dot(string): # 6
    return re.sub(r'[ ,.]', ':', string)

def snake_to_camel(string): # 7
    return ''.join(word.title() if i else word for i, word in enumerate(string.split('_')))

def split_at_uppercase(string): # 8
    return re.split(r'(?=[A-Z])', string)

def insert_spaces_between_capitals(string): # 9
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', string)

def camel_to_snake(string):  # 10
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
