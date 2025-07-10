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

user1 = "FPTU"
pass1 = "69fptunictcamp"
name1 = "Trường đại học FPT Cần Thơ"

user2 = "FSC"
pass2 = "69fptschctcamp"
name2 = "Trường THPT FPT Cần Thơ"

organizer = {}
organizer[user1] = {"name": name1, "pass": ceasar_encrypt(pass1)}
organizer[user2] = {"name": name2, "pass": ceasar_encrypt(pass2)}

try:
    with open(pu.ORGS_FILE, "x", encoding= "utf-8") as file:
        json.dump(organizer, file, indent= 4)
except:
    with open(pu.ORGS_FILE, "r", encoding= "utf-8") as file:
        organizer_load = dict(json.load(file))
        #debug only
        #for k, v in organizer.items():
            #print(k, v["name"], ceasar_decrypt(v["pass"]))
    with open(pu.ORGS_FILE, "w", encoding= "utf-8") as file:
        json.dump(organizer, file, indent= 4)
        print("ABC XYZ")