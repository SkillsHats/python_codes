import random
import string

password_length = int(input("Enter the length of the password : "))

# get random string of letters and digits
source = string.ascii_letters + string.digits
password = ''.join((random.choice(source) for _ in range(password_length)))

print("Password : ", password)

