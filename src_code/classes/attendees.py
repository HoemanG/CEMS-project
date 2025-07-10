import sys
import os
import json


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import path_utils as pu
sys.path.append(pu.CLASS_DIR)
sys.path.append(pu.DATA_DIR)
from .events import Event

#store an attendee into 
class Attendee():
    __all_events = {}
    try:
        with open(pu.EVENTS_FILE, "r") as file:
            __all_events = dict(json.load(file))
    except:
        with open(pu.EVENTS_FILE, "x") as file:
            json.dump(__all_events, file, indent= 4)
    def __init__(self, id: str, name, contact, is_student: bool):
        self.name = name
        #can be either an attendee's phone number or personal email
        self.contact = contact
        self.id = id
        self.is_student = is_student
        #1 attendee
        self.__attendee = {self.id: {"name": self.name, "contact": self.contact, "is_student": self.is_student}}
        self.__all_attendees = {}
        #load the guests' and students' database
        try:
            with open(pu.ATDS_FILE, "x", encoding= "utf-8") as file:
                json.dump(self.__all_attendees, file, indent= 4)
        except FileExistsError:
            with open(pu.ATDS_FILE, "r", encoding= "utf-8") as file:
                self.__all_attendees = json.load(file)
        
        #auto check if current attendee's information has been saved 
        if self.id not in self.__all_attendees:
            self.__all_attendees.update(self.__attendee)
            with open(pu.ATDS_FILE, "w", encoding= "utf-8") as file:
                json.dump(self.__all_attendees, file, indent= 4)
        #else is just for if-else symmetry :)
        else:
            pass
        

    

    @classmethod
    #granting access for an attendee
    #guests ID are globally, 
    # which means the same guest code in different events represent the same person
    def login(cls):

        while True:
            is_student = input("Are you a student? [Y/n]: ")
            if is_student.lower() == "y":
                is_student = True
                break
            elif is_student.lower() == "n":
                is_student = False
                break
            else:
                print("Please enter a valid option")
                continue
        try:
            with open(pu.ATDS_FILE, "r", encoding= "utf-8") as file:
                all_attendees = dict(json.load(file))
        except FileNotFoundError:
            print("No attendees' profile found\nPlease try reinstalling the app or contact publisher")
            return False
        


        if is_student:
            student_id = input("Enter your student ID ")
            for k, v in all_attendees.items():
                if student_id == k:
                    return cls(k, v["name"], v["contact"], v["is_student"])
            print("Please enter a valid Student ID")
            return False
        

        
        else:
            guest_exist = input("Do you have a guest ID [Y/n] ").lower() == "y"
            if guest_exist:
                guest_id = input("Enter your guest ID ")
                for k, v in all_attendees.items():
                    if guest_id == k:
                        return cls(k, v["name"], v["contact"], v["is_student"])
                    
                print("Please enter a valid Guest ID")
            else: #generate a guest code
                name = input("Please enter your name ")
                contact = input("Please enter your contact way (can be either phone number or gmail) ")
                count = sum(1 for k in all_attendees if k.startswith("GT"))
                guest_id = f"GT{(count + 1):03}"
                return cls(guest_id, name, contact, is_student)
            
    
    #search for an event using event code, return false if not found
    def evt_search_code(self, input_code: str):
        if input_code in self.__all_events.keys():
            #this should have been used if this method was not reused :(((
            print(f"Event code: {input_code:<15}\t\tEvent name: {self.__all_events[input_code]["name"]:<20}\t\tDate: {self.__all_events[input_code]["date"]:<10}")
            return self.__all_events[input_code]
        else:
            print("Event not found")
            return False
    
    #search for an event using event name, return false if not found
    def evt_search_name(self, input_name: str):
        for k, v in self.__all_events.items():
            if input_name == v["name"]:
                #this is not used because of symmetry :)
                print(f"Event code: {k:<15}\t\tEvent name: {self.__all_events[k]["name"]:<20}\t\tDate: {self.__all_events[k]["date"]:<10}")
                return self.__all_events[k]
        print("Event not found")
        return False
    

    #register an event, return false if event not found or registered failed
    def evt_reg(self, input_code: str):
        if self.evt_search_code(input_code):
            if not self.id in self.__all_events[input_code]["atds"]:
                if ((len(self.__all_events[input_code]["atds"])) >= self.__all_events[input_code]["capacity"]):
                    print("The event is full")
                    return False
                else:
                    self.__all_events[input_code]["atds"].append(self.id)
                    with open(pu.EVENTS_FILE, "w", encoding= "utf-8") as file:
                        json.dump(self.__all_events, file, indent= 4)
                        return True
            else:
            #print lines are used for identify the error
                print("You already registered this event")
                return False
        else:
            #print("Event not found")
            return False
        print("Register failed, please contact the admin")
        return False
    

    #see registered events of an attendees
    def get_reged_evt(self):
        for k, v in self.__all_events.items():
            if self.id in v["atds"]:
                print(f"Registered Event: {v['name']} happens on {v['date']}")
    