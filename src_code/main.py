from attendee_UI import run_atd
from organizer_UI import run_org
from admin_UI import run_adm
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main_menu():
    roles = ["1. Attendee", "2. Organizer", "3. Admin"]
    print(("=")*18)
    for role in roles:
        print(f"||{role:<14}||")
    print(("=")*18)

if __name__ == "__main__":
    while True:
        clear()
        print("★ C.E.M.S ★ - Campus Event Management System")
        main_menu()
        state = int(input("Please enter your role, enter 0 to exit "))

        if state == 0:
            exit()
        

        clear()
        role_actions = {
        1: run_atd,
        2: run_org,
        3: run_adm
        }

        action = role_actions.get(state)
        if action:
            action(state)
        else:
            print("Invalid choice.")