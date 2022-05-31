cont = True
while cont == True:
    print("Display Quadratic Coefficients")
    try:
        a = float(input("Enter a: "))
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
    except (ValueError, TypeError):
        print("It seems one of your inputs is not a number, please try again.")
    
    d = b**2 - 4*a*c
    if not(d > 0 or d < 0):
        print("1 real solution")
    elif d < 0: 
        print("2 complex solutions")
    else:
        print("2 real solutions")

    cont1 = input("Would you like to continue? y/n ")
    yes = ["Y", 'y', 'yes', "Yes"]
    no = ["N", 'n', "No", "no"]
    
    if cont1 in yes:
        cont = True
    else: 
        cont = False