s = input("Enter a string : ")
def isPalindrome(s):
    return s == s[::-1]
if isPalindrome(s):
    print("It is Palindrome!")
else: 
    print("It is not Palindrome.")