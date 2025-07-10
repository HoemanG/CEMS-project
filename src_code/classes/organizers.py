import sys
import os
import datetime as dt
import json
import csv
import random as rand


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import path_utils as pu
sys.path.append(pu.CLASS_DIR)
sys.path.append(pu.DATA_DIR)
from .events import Event

class Organizer():
    
    __org_data = {}
    __all_events = {}

    try:
        with open(pu.ORGS_FILE, "r", encoding= "utf-8") as file:
            __org_data = dict(json.load(file))
    except:
        print("Organizers data not found, please try reinstalling the app or contact the admin")

    def __init__(self, name, org_id, password):
        self.name = name
        self._org_id = org_id
        self.__password = password
        try:
            with open(pu.ORGS_FILE, "r", encoding= "utf-8") as file:
                self.__org_data = dict(json.load(file))
        except:
            with open(pu.ORGS_FILE, "r", encoding= "utf-8") as file:
                json.dump(self.__org_data, file, indent= 4)

        try:
            with open(pu.EVENTS_FILE, "r", encoding= "utf-8") as file:
                self.__all_events = dict(json.load(file))
        except:
             with open(pu.EVENTS_FILE, "r", encoding= "utf-8") as file:
                json.dump(self.__all_events, file, indent= 4)
    

    #login as organizer, return false if login failed
    @classmethod
    def login(cls):

        user = input("Please enter your Organizer ID ")
        password = input("Please enter your password ")

        for k, v in cls.__org_data.items():
            if user == k and password == ceasar_decrypt(v["pass"]):
                return cls(v["name"], user, password)
        
        print("Password or username was wrong, please check your spelling and try again")
        return False
    
    def add_evt(self):

        name = input("Please enter the name of the event ")
        date = input("Please enter the date the event happens (dd/mm/yy) ")
        cap = int(input("Please enter the capacity of your planned event in integer "))

        #check if capacity is a valid input
        if cap < 1:
            print("Capacity of an event must be equal to or greater than 1")
            return False

        evt = Event(name, self._org_id, date, cap, [])

        evt.code_gen()

        evt.info_to_dict_evt()
        
        #get the event code and check if the event existed in the system
        event_code = list(evt._cur_evnt.keys())[0]
        if event_code in evt._all_evnt:
            choice = input("This event already exists in the system. Continuing will overwrite it. Do you want to proceed? [Y/n]: ").lower()
            if choice != "y":
                print("Event creation canceled")
                return False
    
    
        
        evt.get_evt_data()
        evt.update_new_to_old()
        #update_new_to_old update the __all_evnt dict by the _cur_evnt dict
        #so this "existing" will be legit 
        existing = self.__all_events.get(event_code)
        if existing and len(existing["atds"]) > cap:
            print(f"Cannot reduce capacity below current number of attendees ({len(existing['atds'])}).")
            #the _all_evnt dict are auto re-load and changes are not saved if it is not saved to the file
            #so there is no need to add another with open() function here
            return False

        evt.update_evt_to_json()
        evt.get_evt_data()
        self.__all_events = evt.get_evt_data()


    #delete an event of theirs, return wheter the event is deleted or not
    def del_evt(self):
        code = input("Enter the event code you want to delete ")
        for k, v in self.__all_events.items():
            if self._org_id == v["org_id"] and code == k:
                del self.__all_events[code]
                with open(pu.EVENTS_FILE, "w") as file:
                    json.dump(self.__all_events, file, indent= 4)
                    print("Event deleted successfully")
                    return True
        print("Event code not found")
        return False
    #view the org's events and their details
    def evnt_view(self):
        for k, v in self.__all_events.items():
            if self._org_id == v["org_id"]:
                print(f"Event code: {k:<15}\tEvent name: {v["name"]:<20}\thappens on: {v["date"]:<20}\tnow has: {len(v["atds"])}/{v["capacity"]}")


    #view information of an attendee of their event
    #return the information of the attendee, false if not found
    def atd_view(self):
        input_id = input("Enter an ID you want to find ")
        for k, v in self.__all_events.items():
            if input_id in v["atds"] and self._org_id == v["org_id"]:
                with open(pu.ATDS_FILE, "r", encoding= "utf-8") as file:
                    atd_data = dict(json.load(file))
                    print(atd_data[input_id])
                    return True
        else:
            print("ID not found or the attendee does not attend any of your events")
            return False
        

    #remove an attendee from their events
    def atd_rm(self):
        input_id = input("Enter an ID you want to remove ")
        input_code_evt = input("Enter the code of the event that you want the attendee to be removed from ")
        for k, v in self.__all_events.items():
            if input_id in v["atds"] and self._org_id == v["org_id"]:
                if k == input_code_evt:
                    self.__all_events[k]["atds"].remove(input_id)
                    return True
        print("Attendee ID or Event code not found, please re-check your spelling")
        return False
    

    #export statistical report of the org's events
    def exprt_evt(self):
        field = ["Event Code", "Event Name", "Date", "Capacity", "Attendees", "Attendance rate"]
        rows = []
        for k, v in self.__all_events.items():
            if v["org_id"] == self._org_id:
                row = [k, v["name"], v["date"], v["capacity"], str(len(v["atds"])), f"{(len(v['atds']) / v['capacity']) * 100:.1f}%"]
                rows.append(row)

        try:
            with open(pu.ORG_STAT_FILE, "x", newline= "") as file:
                writer = csv.writer(file)
                writer.writerow(field)
                writer.writerows(rows)
                print("A report has been exported successfully")

        except:
            with open(pu.ORG_STAT_FILE, "w", newline= "") as file:
                writer = csv.writer(file)
                writer.writerow(field)
                writer.writerows(rows)
                print("A report has been exported successfully")


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