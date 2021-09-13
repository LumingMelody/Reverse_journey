# from hashlib import sha1
import hashlib

password = "123456"

# s1 = sha1()

print(hashlib.sha1(password.encode(encoding='UTF-8')).hexdigest())

str1 = 'fbc8c168e3188a7ee23e7e391b266440b2c9d384'
print(len(str1))
