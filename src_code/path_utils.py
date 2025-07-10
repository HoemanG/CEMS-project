#store basic paths
from pathlib import Path

#this is ~\src_code
BASE_DIR = Path(__file__).resolve().parent
#this is ~\src_code\...
DATA_DIR = BASE_DIR / "data"
CLASS_DIR = BASE_DIR / "classes"
TEXT_DIR = BASE_DIR / "text_art"
#this is path to the events.json file or ~\src_code\data\events.json
EVENTS_FILE = DATA_DIR / "events.json"
#this is path to statistical exported (admin) file
STAT_FILE = DATA_DIR / "stat_report.csv"
#this is path to statistical exported (organizer) file
ORG_STAT_FILE = DATA_DIR / "org_stat_report.csv"
#This is path to the admins' profiles
ADMINS_FILE = DATA_DIR / "admins.json"
#this is path to students' and guests' profiles
ATDS_FILE = DATA_DIR / "atds.json"
#this is path to organizers' profile
ORGS_FILE = DATA_DIR / "orgs.json"

ADMIN_TEXT = TEXT_DIR / "admin.txt"
ORG_TEXT = TEXT_DIR / "organizer.txt"
ATD_TEXT = TEXT_DIR / "attendee.txt"