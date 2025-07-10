
import sys
import os
import datetime as dt
import json

#the path will be ~\src_code
#print(os.path.dirname(os.path.dirname(__file__)))
#fix the path so we can import modules from ~\src_code also, but not just ~\src_code\classes
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import path_utils as pu


class Event():
    
    #init an event
    def __init__(self, name, organizer_id,date, capacity, attendees, code = None):
        self.code = code
        self.name = name
        #date of the event in dd/mm/yyyy format
        self.date = date
        self.cap = capacity
        #org id
        self._org_id = organizer_id
        #list of all attendees of the event
        self._atd = attendees
        #a dict of the current event
        self._cur_evnt = dict()
        #a dict of all the saved evt
        self._all_evnt = dict()
        pass
    
    #generate the code for an event
    def is_valid_date(self, fmt = "%d/%m/%Y"):
        try:
            dt.datetime.strptime(self.date, fmt)
        except:
            return False
        return True

    #prefix will be the organizer's id
    #change only the code of the event, no savings done
    def code_gen(self, prefix= None):
        prefix = self._org_id
        if not self.is_valid_date():
            print("Invalid format or date")
            return

        # Convert date string to datetime object
        date_obj = dt.datetime.strptime(self.date, "%d/%m/%Y")

        # Load existing events
        try:
            with open(pu.EVENTS_FILE, "r", encoding="utf-8") as file:
                self._all_evnt = json.load(file)
        except:
            self._all_evnt = {}

        #Check for duplicate: same name and same date
        for code, event in self._all_evnt.items():
            if event["name"] == self.name and event["date"] == self.date:
                #print only for debug
                #print(f"[!] Event '{self.name}' on {self.date} already exists with code {code}. Skipping creation.")
                self.code = code  # reuse existing code
                return

        # Count how many events already exist on that date
        count_of_day = sum(1 for e in self._all_evnt.values() if e["date"] == self.date)
        self.code = (f"{prefix}{date_obj.strftime('%Y%m%d')}_{(count_of_day + 1):03}")
        return
    
    def info_to_dict_evt(self):
        self._cur_evnt[self.code] = {
        "name": self.name,
        "date": self.date.strftime("%d/%m/%Y") if isinstance(self.date, dt.datetime) else self.date,
        "capacity": self.cap,
        "org_id": self._org_id,
        "atds": self._atd
        }
        return self._cur_evnt


    #update the current event to all events dict
    def update_new_to_old(self):
        self._all_evnt.update(self._cur_evnt)


    #save all events to a json file
    def update_evt_to_json(self):
        #re-update again to ensure newest data saved
        self._all_evnt.update(self._cur_evnt)

        #create a file if no data.json found
        try:
            #the "x" is kinda useless, that's kinda what is the try-except for
            with open(pu.EVENTS_FILE, "x", encoding= "utf-8") as file:
                json.dump(self._all_evnt, file, indent= 4)
        
        #else overwrite the file
        except FileExistsError:
            with open(pu.EVENTS_FILE, "r", encoding= "utf-8") as file:
                self._all_evnt = dict(json.load(file))
                self._all_evnt.update(self._cur_evnt)
            with open(pu.EVENTS_FILE, "w", encoding= "utf-8") as file:
                json.dump(self._all_evnt, file, indent= 4)

    #extract the events file to a dictionary
    def get_evt_data(self):
        try:
            with open(pu.EVENTS_FILE, "r", encoding= "utf-8") as file:
                self._all_evnt = dict(json.load(file))
                return self._all_evnt
        except:
           return ("Old data retrieval failed")
    