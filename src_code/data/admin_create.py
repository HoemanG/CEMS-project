import random as rand
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import path_utils as pu
import json

#encrypt the admin's password using ceasar's method
def ceasar_encrypt(input: str, shift = None):
    if shift == None:
        #shift argument will take exactly 2 digits
        shift = rand.randint(10, 26)

    password = ""
    for char in input:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            password += chr((ord(char) - base + shift) % 26 + base)
        else:
            password += char
    result = str(shift) + password
    return result


#decrypt the admin's password using ceasar's method
def ceasar_decrypt(input:str):
    result = ""
    shift = int(input[:2])
    encrypted = input[2:]
    result = ceasar_encrypt(encrypted, -shift)[3:]
    return result

user1 = "NhanPTCE200090"
pass1 = "90nhanabc"
name1 = "Phan Trọng Nhân"

user2 = "NhungNTH69"
pass2 = "60nhungabc"
name2 = "Nguyễn Thị Hồng Nhung"

admin = {}
admin[user1] = {"name": name1, "pass": ceasar_encrypt(pass1)}
admin[user2] = {"name": name2, "pass": ceasar_encrypt(pass2)}

try:
    with open(pu.ADMINS_FILE, "x", encoding= "utf-8") as file:
        json.dump(admin, file, indent= 4)
except:
    with open(pu.ADMINS_FILE, "r", encoding= "utf-8") as file:
        admin_load = dict(json.load(file))
        #debug only
        #for k, v in admin.items():
            #print(k, v["name"], ceasar_decrypt(v["pass"]))
    with open(pu.ADMINS_FILE, "w", encoding= "utf-8") as file:
        json.dump(admin, file, indent= 4)
        print("ABC XYZ")