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

class Admin():
    def __init__(self, name, username, password):
        self.name = name
        self.__username = username
        self.__password = password
        self.__last_created = None
        try:
            with open(pu.EVENTS_FILE, "r") as file:
                self.__all_events = json.load(file)
        except FileNotFoundError:
            with open(pu.EVENTS_FILE, "x") as file:
                json.dump(self.__all_events, file, indent= 4)

    
    #view all events and their details
    def evt_view(self):
        for k, v in self.__all_events.items():
            print(f"The event {v["name"]} with the code {k} is organized by {v["org_id"]} has {len(self.__all_events[k]["atds"])} attendees")

    #no need to pre-input the code of the event
    #auto update to the Event._all_evnt but not to json file
    #if adding an existed event, it will overwrite the old one
    #return an event object
    def add_evt(self, name, organizer_id, date, capacity, attendees, code = None):

        #check if capacity is a valid input
        if capacity < 1:
            print("Capacity of an event must be equal to or greater than 1")
            return False
        
        if len(attendees) > capacity:
            print(f"Cannot create an overloaded with attendees event.")
            return False

        #evt now is just an object whose attributes are status of the event
        evt = Event(name, organizer_id, date, capacity, attendees, code)

        #generate an event code
        evt.code_gen()

        #create a diction of the current event
        evt.info_to_dict_evt()

        #get the event code and check if the event existed in the system
        event_code = list(evt._cur_evnt.keys())[0]
        if event_code in evt._all_evnt:
            choice = input("This event already exists in the system. Continuing will overwrite it. Do you want to proceed? [Y/n]: ").lower()
            if choice != "y":
                print("Event creation canceled")
                return False    
        
        #add the current event to all evt dict()    
        evt.update_new_to_old()

        #if overwriting/creating an overloaded event, it will leave a message and return False
        existing = self.__all_events.get(event_code)
        if existing and len(existing["atds"]) > capacity:
            print(f"Cannot reduce capacity below current number of attendees ({len(existing['atds'])}).")
            return False
        
        evt.update_evt_to_json()
        self.__last_created = evt
        #__all_events holds also the last created event
        self.__all_events = Event.get_evt_data(evt)
        return evt


    #make sure the input code of the event exists
    def find_evt(self, code_to_find: dict):
        for code, info in self.__all_events.items():
            if code == code_to_find:
                return True
        return False
    
    #delete an event, auto store to the file and edit the dictionary
    def del_evt(self, input_code):
        if self.find_evt(input_code):
            del self.__all_events[input_code]
            with open(pu.EVENTS_FILE, "w", encoding= "utf-8") as file:
                json.dump(self.__all_events, file, indent= 4)
        else:
            print("Input code not found")
    
    #track event capacity (person/max_person)
    def evt_track_cap(self, input_code):
        if self.find_evt(input_code):
            print(f"Event {self.__all_events[input_code]["name"]} now has {len(self.__all_events[input_code]["atds"])}/{self.__all_events[input_code]["capacity"]}")
        else:
            print("Input code not found")

    #login as an admin
    @classmethod
    #claasmethods are methods that creates/return a class
    #cls means class
    def login(cls):
        try:
            with open(pu.ADMINS_FILE, "r", encoding= "utf-8") as file:
                admin_data = dict(json.load(file))
        except FileNotFoundError:
            print("No admin data found, please try re-installing the app or contact publisher")
            return False
        
        user_in = input("Enter your username ")
        pass_in = input("Enter your password ")
        
        if user_in in admin_data.keys():
            password = ceasar_decrypt(admin_data[user_in]["pass"])
            if pass_in == password:
                name = admin_data[user_in]["name"]
                print(f"Welcome admin {name}")
                return cls(name, user_in, pass_in)
            else:
                print("You entered wrong password")
                return False
        else:
            print("username not exist")
            return False
        #note: both print lines should be "You entered wrong password or username"
        #but here, they are different just for clarity in login fail and success

    #calculate sum of attendees across all event
    def evt_calculate(self):
        all_atd, low, high = 0, float("inf"), -float("inf")
        code_low = ""
        code_high = ""
        for k, v in self.__all_events.items():
            all_atd += len(v["atds"])
            if len(v["atds"]) < low:
                low = len(v["atds"])
                code_low = k
            if len(v["atds"]) > high:
                high = len(v["atds"])
                code_high = k
        print(f"The event with lowest attendance is {self.__all_events[code_low]["name"]} with {low} attendees")
        print(f"The event with highest attendance is {self.__all_events[code_high]["name"]} with {high} attendees")
        return all_atd
    

    #export statistical report
    # Note: this will overwrite the existing report file with the latest data.
    def exprt_stat(self):
        field = ["Event Code", "Event Name", "Date", "Capacity", "Attendees", "Attendance rate"]
        rows = []
        for k, v in self.__all_events.items():
            row = [k, v["name"], v["date"], v["capacity"], str(len(v["atds"])), f"{(len(v['atds']) / v['capacity']) * 100:.1f}%"]
            rows.append(row)
        try:
            with open(pu.STAT_FILE, "x", newline= "") as file:
                writer = csv.writer(file)
                writer.writerow(field)
                writer.writerows(rows)
                print("A report has been exported successfully")
        except:
            with open(pu.STAT_FILE, "w", newline= "") as file:
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
