import random as rnd
import string

#Main logic For generating password
def main(pass_len):
    char_list = string.ascii_letters + string.digits + string.punctuation #For making a list of all char
    password = "".join(rnd.choice(char_list) for i in range(pass_len)) #Join the password by randomly selecting character
    return password


if __name__ == '__main__':
    pass_length = int(input("Enter Password Length: ")) #Take input from user
    print(f"Your Generated Password: {main(pass_length)}")
