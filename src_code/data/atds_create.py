import random as rand
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import path_utils as pu
import json


#stu
atd = {"CE200090": {"name": "Phan Trọng Nhân", "contact": "example@fpt.edu.vn", "is_student": True}}
#gt
atd.update({"GT001": {"name": "Dullahan Gan Ceann", "contact": "Headless_knight_Dullahan@gmail.com", "is_student": False}})


with open(pu.ATDS_FILE, "x", encoding= "utf-8") as file:
    json.dump(atd, file, indent= 4)