import webbrowser
import datetime
import os

def open_local_calendar():
    # Option 1: Try to open Windows Calendar
    try:
        os.system("start outlookcal:")
    except:
        # Option 2: Fallback to system clock settings or local calendar HTML (offline)
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        print(f"Offline calendar: {today}")
        return f"Offline calendar: {today}"

