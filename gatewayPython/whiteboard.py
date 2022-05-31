# import numpy as np
# import bokeh.plotting
# import bokeh.io

# bokeh.io.output_notebook()

# # Generate plotting values
# t = np.linspace(0, 2*np.pi, 200)
# x = 16 * np.sin(t)**3
# y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

# p = bokeh.plotting.figure(height=250, width=275)
# p.line(x, y, color='red', line_width=3)
# text = bokeh.models.Label(x=0, y=0, text='bootcamp', text_align='center')
# p.add_layout(text)

# bokeh.io.show(p)

# class Account:
#     def __init__(self, owner, balance):
#         assert type(owner) == str
#         assert type(balance) == int or float
#         self.owner = owner
#         self.balance = balance
#         self.hist = [balance]
    
#     def __repr__(self) -> str:
#         return f"{self.owner}'s account contains ${self.balance:.2f} dollars"

#     def getBalance(self):
#         return self.balance
    
#     def withdraw(self, withdrawal):
#         withdraw = self.balance - withdrawal
#         self.hist.append(withdraw)
#         return withdraw
    
#     def deposit(self, deposit):
#         depositval = self.balance + deposit
#         self.hist.append(depositval)
#         return depositval
    
#     def getHistory(self):
#         return self.hist

#     def transferTo(self, other, transfer):
#         self.balance -= transfer
#         other.balance += transfer

# class SavingsAccount(Account):
#     def __init__(self, owner, balance, interestRate):
#         super().__init__(owner, balance)
#         self.rate = interestRate / 100
    
#     def getInterestRate(self):
#         return self.rate
    
#     def addInterest(self):
#         self.balance *= 1 + self.rate
#         self.hist.append(self.balance)
#         return self.balance

def getAge(age):
    try:
        n = float(age)
        (n > 0) == 1
        print("you are " + age + " years young!")
    except ValueError:
        print("Incorrect Value inputted")
    except TypeError:
        print("Incorrect type inputted")

age = input("Enter number: ")
getAge(age)