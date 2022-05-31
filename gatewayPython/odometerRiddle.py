"""
@author: Siamak Ardekani
"""

def isPalindrome(s):
    """
    Checks if a string is a palindrome

    Parameters
    ----------
    s : str

    Returns
    -------
    bool
        True if s is a palindrome, otherwise False.
    """
    return s == s[-1::-1]

def check_six_digit_odometer():
    """
    Solves the palindrome riddle.
    """
    
    for i in range(1000000):
        if isPalindrome("{0:06d}".format(i)[2::]) and \
           isPalindrome("{0:06d}".format(i+1)[1::]) and \
           isPalindrome("{0:06d}".format(i+2)[1:-1]) and \
           isPalindrome("{0:06d}".format(i+3)):
               print('\n',i)
               
if __name__=="__main__": 
    check_six_digit_odometer()
