try:
    leap = int(input("Enter a leap year: "))
    numleap = int(input("Enter a # of leap years: "))
except (ValueError, TypeError):
    print("You did not type an integer year, please try again")
    quit()

lp = False

if leap%100 == 0 and leap%400 == 0:
    print("Rare Leap Year")
    lp = True
elif leap%4 == 0:
    print("Leap Year")
    lp = True
else:
    print("Not Leap Year")

leapyears = list()

if lp == True:
    for i in numleap