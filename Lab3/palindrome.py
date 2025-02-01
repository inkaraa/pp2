def is_palindrome(s):
    s = s.replace(" ", "").lower()  
    return s == s[::-1]  

print(is_palindrome("madam"))  
print(is_palindrome("hello"))  
print(is_palindrome("racecar"))  
print(is_palindrome("A man a plan a canal Panama")) 