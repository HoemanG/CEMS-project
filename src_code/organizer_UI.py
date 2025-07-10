from classes.organizers import Organizer
import os
import path_utils as pu

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def org_menu():

    try:
        with open(pu.ORG_TEXT, "r") as file:
            text = file.read()
        print(text)
    except:
        pass
    
    methods = ["View all of your created event", "View information of an attendee of your event",
               "Remove an attendee from your events", "Add new event under your name", 
               "Delete one of your events", 
               "Export a statistical report of your events", "Logout", "Exit"]
    
    print(("=")*60)
    for num, med in enumerate(methods):
        line = f"{num + 1}.{med}"
        print(f"||{line:<56}||")
    print(("=")*60)




def run_org(state):
    while state == 2 or state == 2.5:
        if state == 2:
            org = Organizer.login()


        #if login false, re-login
        if not org:
            continue
            
        state = 2.5
        clear()
        org_menu()
        
        try:
            feat_num = int(input("Enter the function you want to execute "))
        except ValueError:
            print("Please enter a valid option ")
            input("Press any key to continue ")
            state = 3.5
        
        def logout():
            print("Loggin' out ...")


        actions = {
        1: org.evnt_view, #or we can use lambda: org.evnt_view(), same for the rest
        2: org.atd_view,  #when we call a method/function without (), 
        3: org.atd_rm,    # it does not run but points to where method/function is
        4: org.add_evt,
        5: org.del_evt,
        6: org.exprt_evt,
        7: logout,
        8: exit
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
    run_org(2)