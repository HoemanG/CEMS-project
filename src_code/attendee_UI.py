from classes.attendees import Attendee
import os
import path_utils as pu

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def atd_menu():

    try:
        with open(pu.ATD_TEXT, "r") as file:
            text = file.read()
        print(text)
    except:
        pass

    methods = ["Search Event by code",
               "Search Event by name",
               "Register an event by code",
               "View registerd event",
               "Logout", "Exit"]
    print(("=")*45)
    for num, med in enumerate(methods):
        line = f"{num + 1}.{med}"
        print(f"||{line:<41}||")
    print(("=")*45) 
    


def run_atd(state):
    while state == 1 or state == 1.5:

        if state == 1:
            atd = Attendee.login()

        if not atd:
            continue
        
        state = 1.5
        clear()
        atd_menu()

        try:
            feat_num = int(input("Enter the function you want to execute "))
        except ValueError:
            print("Please enter a valid option ")
            input("Press any key to continue ")
            state = 1.5

        def logout():
            print("Loggin' out ...")
            #setattr(globals(), 'state', 0)

        actions = {
            1: lambda: atd.evt_search_code(input_code= input("Please enter the code of the event ")),
            2:  lambda: atd.evt_search_name(input_name= input("Please enter the name of the event ")),
            3: lambda: atd.evt_reg(input_code= input("Please enter the code of the event you want to register ")),
            4: atd.get_reged_evt,
            5: logout,
            6: exit
        }

        action = actions.get(feat_num)

        if action:
            action()
            print("\n" + "=" * 45)
            input("Press any key to continue ")
            if feat_num == 5:
                state = 0.5
        else:
            print("Please enter a valid choice")
            input("Press any key to continue ")

if __name__ == "__main__":
    run_atd(1)