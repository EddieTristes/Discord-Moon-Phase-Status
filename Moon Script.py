import ephem
import requests
import json
import time
from datetime import datetime, timedelta, timezone

token = ""  # Put your Discord Token here. You can learn how at https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md

iteration_count = 1

def get_moon_phase():
    observer = ephem.Observer()
    current_date = datetime.now(timezone.utc).date()
    observer.date = current_date
    moon = ephem.Moon(observer)
    illumination = moon.moon_phase * 100

    next_new_moon_date = ephem.next_new_moon(observer.date).datetime().date()
    next_first_quarter_date = ephem.next_first_quarter_moon(observer.date).datetime().date()
    next_full_moon_date = ephem.next_full_moon(observer.date).datetime().date()
    next_last_quarter_date = ephem.next_last_quarter_moon(observer.date).datetime().date()

    observer_date = observer.date.datetime().date()

    if observer_date == next_new_moon_date:
        return "New Moon"
    elif observer_date == next_first_quarter_date:
        return "First Quarter"
    elif observer_date == next_last_quarter_date:
        return "Third Quarter"
    elif observer_date == next_full_moon_date:
        return "Full Moon"
    elif observer_date < next_full_moon_date and observer_date < next_new_moon_date:
        return "Waxing Crescent" if illumination < 50 else "Waxing Gibbous"
    elif observer_date > next_full_moon_date and observer_date > next_new_moon_date:
        return "Waning Crescent" if illumination < 50 else "Waning Gibbous"

def resolve_icon(phase_name):
    emoji_dict = {
        "New Moon": "🌑",
        "Waxing Crescent": "🌒",
        "First Quarter": "🌓",
        "Waxing Gibbous": "🌔",
        "Full Moon": "🌕",
        "Waning Gibbous": "🌖",
        "Third Quarter": "🌗",
        "Waning Crescent": "🌘"
    }
    return emoji_dict.get(phase_name, "")

def update_custom_status(message, emoji):
    url = "https://discord.com/api/v8/users/@me/settings"
    header = {
        "Authorization": token
    }

    jsonData = {
        "status": "online",
        "custom_status":{
          "text": message,
          "emoji_name": emoji
        }
    }
    request = requests.patch(url, headers=header, json=jsonData)
    data = request.json()
    return data

def perform_initial_update():
    phase_name = get_moon_phase()
    print("===== Initial Update =====")
    
    phase_name = get_moon_phase()
    observer = ephem.Observer()
    observer.date = ephem.now()
    moon = ephem.Moon(observer)
    moon.compute()

    illumination_percentage = moon.moon_phase * 100
    print("Current moon illumination:", illumination_percentage)
    print("Current moon phase:", phase_name)
    illumination_formatted = "{:.0f}".format(illumination_percentage)

    message = f"Current phase is a {phase_name}! The moon's illumination is {illumination_formatted}%"
    emoji = resolve_icon(phase_name)

    print("Updating custom status...")
    update_custom_status(message, emoji)
    print("Custom status updated.")
    print("==========================")

def main():
    global iteration_count
    perform_initial_update()

    while True:
        now = datetime.now() - timedelta(hours=6)

        if now.minute == 0:
            print("===== Hourly Update =====")
            print("Checking for moon phase update...")

            phase_name = get_moon_phase()
            observer = ephem.Observer()
            observer.date = ephem.now()
            moon = ephem.Moon(observer)
            moon.compute()

            illumination_percentage = moon.moon_phase * 100
            print("Current moon illumination:", illumination_percentage)
            print("Current moon phase:", phase_name)
            illumination_formatted = "{:.0f}".format(illumination_percentage)

            message = f"Current phase is a {phase_name}! The moon's illumination is {illumination_formatted}%"
            emoji = resolve_icon(phase_name)

            print("Updating custom status...")
            update_custom_status(message, emoji)
            print("Custom status updated! Waiting an hour to change status...")
            print("==========================")

            time.sleep(3600)
            iteration_count = 1
        else:
            print(f"(Iteration {iteration_count}) Not the beginning of the hour. Checking again in a minute...")
            time.sleep(60)
            iteration_count += 1

if __name__ == "__main__":
    main()
