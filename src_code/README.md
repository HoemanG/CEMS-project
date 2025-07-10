# Campus Event Management System (C.E.M.S)

This project is a command-line interface (CLI) application for managing campus events. It provides different functionalities based on user roles: Attendee, Organizer, and Admin.

## Features

The system is designed to cater to three distinct user roles, each with a specific set of permissions and capabilities.

### Admin
- View a comprehensive list of all events in the system.
- Add new events.
- Delete existing events.
- Monitor the capacity and attendance of any event.
- Calculate and view attendance statistics across all events, including identifying those with the highest and lowest attendance.
- Export a statistical report of all events to a CSV file.

### Organizer
- View all events created by them.
- Add new events under their organization's name.
- Delete events they have created.
- View the details of attendees registered for their events.
- Remove an attendee from one of their events.
- Export a statistical report for their events to a CSV file.

### Attendee
- Search for available events by event code or name.
- Register for an event.
- View a list of all events they are registered for.
- Login as a student with a student ID or as a guest. New guest IDs are generated automatically.

## System Architecture

The system's design is documented through a series of UML diagrams, which can be found in the `../Document/` directory.

### Flowchart

The main application flow begins at `main.py`. The user is prompted to select their role. Based on the selection, the system transitions to the appropriate state and displays the corresponding user interface.

*(Placeholder for Flowchart Diagram: `../Document/PFP191_ASG-Flowchart.drawio.svg`)*
![Flowchart](./../Document/PFP191_ASG-Flowchart.drawio.svg)

### Class Diagram

The system is composed of four main classes: `Event`, `Admin`, `Organizer`, and `Attendee`. The `Event` class is central, holding all event-related information. The `Admin`, `Organizer`, and `Attendee` classes define the roles and interactions within the system.

*(Placeholder for Class Diagram: `../Document/PFP191_ASG-Class.drawio.svg`)*
![Class Diagram](./../Document/PFP191_ASG-Class.drawio.svg)

### State Diagrams

State diagrams detail the specific workflows and state transitions for each user role after logging in.

-   **Attendee State Diagram:** Shows the flow for an attendee searching, registering, and viewing events.
    *(Placeholder for Attendee State Diagram: `../Document/PFP191_ASG-state 1 - attendees.drawio.svg`)*
    ![Attendee State Diagram](./../Document/PFP191_ASG-state%201%20-%20attendees.drawio.svg)

-   **Organizer State Diagram:** Shows the flow for an organizer managing their events and attendees.
    *(Placeholder for Organizer State Diagram: `../Document/PFP191_ASG-state 2 - organizer.drawio.svg`)*
    ![Organizer State Diagram](./../Document/PFP191_ASG-state%202%20-%20organizer.drawio.svg)

-   **Admin State Diagram:** Shows the flow for an admin overseeing the entire system.
    *(Placeholder for Admin State Diagram: `../Document/PFP191_ASG-state 3 - admin.drawio.svg`)*
    ![Admin State Diagram](./../Document/PFP191_ASG-state%203%20-%20admin.drawio.svg)


## How to Run

1.  Navigate to the `src_code` directory.
2.  Ensure you have Python installed.
3.  Run the application using the following command:
    ```sh
    python main.py
    ```
4.  Follow the on-screen prompts to select your role and interact with the system.

## File Structure

The `src_code` directory is organized as follows:

```
.
├── classes/
│   ├── admin.py       # Admin class definition and methods
│   ├── attendees.py   # Attendee class definition and methods
│   ├── events.py      # Event class definition and methods
│   └── organizers.py  # Organizer class definition and methods
├── data/
│   ├── admins.json    # Stores admin credentials
│   ├── atds.json      # Stores attendee information
│   ├── events.json    # Stores all event data
│   └── orgs.json      # Stores organizer credentials
│   └── *.csv          # Stores exported reports
├── text_art/
│   ├── admin.txt      # ASCII art for admin UI
│   ├── attendee.txt   # ASCII art for attendee UI
│   └── organizer.txt  # ASCII art for organizer UI
├── admin_UI.py        # Handles the command-line interface for Admins
├── attendee_UI.py     # Handles the command-line interface for Attendees
├── organizer_UI.py    # Handles the command-line interface for Organizers
├── main.py            # Main entry point of the application
├── path_utils.py      # Manages file paths for the project
└── README.md          # This file
```
