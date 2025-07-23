#Add Two Number
def add_num(num1, num2):
    return num1 + num2

#Subtract Two Number
def sub_num(num1, num2):
    return num1 - num2

#Multiply Two Number
def mul_num(num1, num2):
    return num1 * num2

#Divide Two Number
def div_num(num1, num2):
    return num1 / num2

class Calculator:
    def __init__(self):
        self.num_1 = 0
        self.num_2 = 0
        self.choice = ""
        self.operaotor_list = ["+","-","*","/"]

    #Will Greet the User
    @staticmethod
    def greet():
        print("Welcome to Calculator")
        print("-"*50)
        print("-"*50)

    #Take input from user
    def input(self):
        print("Please enter your 1st number:",end=" ")
        self.num_1 = int(input())
        print("Please enter your 2nd number:",end=" ")
        self.num_2 = int(input())


    #Take operator choice from user
    def operator(self):
        print("Please enter your choice (+,-,*,/):",end=" ")
        self.choice = input()

    #Do the all work
    def calculate(self):
        if self.choice == "+":
            print(f"Final answer = {add_num(self.num_1, self.num_2)}")
        if self.choice == "-":
            print(f"Final answer = {sub_num(self.num_1, self.num_2)}")
        if self.choice == "*":
            print(f"Final answer = {mul_num(self.num_1, self.num_2)}")
        if self.choice == "/":
            print(f"Final answer = {div_num(self.num_1, self.num_2)}")

    @staticmethod
    def exit_cal():
        print()
        print("Thank you for using Calculator")
        print("-"*50)
        print("-"*50)

if __name__ == "__main__":
    app = Calculator()
    app.greet()
    cal_exit = 0
    try:
        while True:
            ope = 0
            try:
                app.input()
            except ValueError:
                print("You didn't enter a number")
                continue
            while ope == 0:
                app.operator()
                if app.choice in app.operaotor_list:
                    ope = 1
                else:
                    print("Enter a valid operator")
            try:
                app.calculate()
            except ZeroDivisionError:
                print("You can't divide by zero")
            print("-"*50)
            #Choose want to Continue or Not
            while True:
                print("Want to continue? (y/n):",end=" ")
                con_choice = input().lower()
                if con_choice == "y":
                    pass
                    break
                elif con_choice == "n":
                    cal_exit = 1
                    break
                else:
                    print("Enter a valid choice")
            if cal_exit == 1:
                app.exit_cal()
                break

    #For not throwing error if stop the program
    except KeyboardInterrupt:
        app.exit_cal()
