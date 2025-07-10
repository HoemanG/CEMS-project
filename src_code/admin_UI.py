from classes.admin import Admin
import os
import path_utils as pu

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def admin_menu():
    try:
        with open(pu.ADMIN_TEXT, "r") as file:
            text = file.read()
        print(text)
    except:
        pass


    methods =  ["View all events", "Add a new event", "Delete an event", 
                "Track capacity of an event", 
                "Calculate all attendance across all events and which with lowest and highest attendance",
                "Export statistical report to a csv file", "Log out", "Exit the program"]
    maxlen = len(methods[4])
    print(("=")*(maxlen+7))
    for num, med in enumerate(methods):
        line = f"{num + 1}.{med}"
        print(f"||{line:<90}||")
    print(("=")*(maxlen+7))

def run_adm(state):
    while state == 3 or state == 3.5:
        
        if state == 3:
            adm = Admin.login()

        #if login false, re-login
        if not adm:
            continue
        
        state = 3.5
        clear()
        admin_menu()
        try:
            feat_num = int(input("Enter the function you want to execute "))
        except ValueError:
            print("Please enter a valid option ")
            input("Press any key to continue ")
            state = 3.5

        def logout():
            print("Loggin' out ...")
        

        actions = {
        1: lambda: adm.evt_view(),
        2: lambda: adm.add_evt(
            input("Event name: "),
            input("Organizer ID: "),
            input("Date (dd/mm/yy): "),
            int(input("Capacity: ")),
            []
        ),
        3: lambda: adm.del_evt(input("Event code to delete: ")),
        4: lambda: adm.evt_track_cap(input("Event code to track: ")),
        5: lambda: print(f"Total attendance: {adm.evt_calculate()}"),
        6: lambda: adm.exprt_stat(),
        7: lambda: logout(),
        8: lambda: exit()
        }

        action = actions.get(feat_num)
        if action:
            action()
            print("\n" + "=" * 60)
            input("Press any key to continue ")
            if feat_num == 7:
                state = 0.5
        else:
            print("Please enter a valid choice")
            input("Press any key to continue ")

if __name__ == "__main__":
    run_adm(3)