import ephem
import requests
import json
import time
from datetime import datetime, timedelta

token = "" #Put your Discord Token here. You can learn how at https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md

iteration_count = 1

def get_moon_phase():
    observer = ephem.Observer()
    observer.date = ephem.now()
    moon = ephem.Moon(observer)

    illumination = moon.moon_phase * 100

    next_new_moon_date = ephem.next_new_moon(observer.date)

    next_first_quarter_date = ephem.next_first_quarter_moon(observer.date)

    next_full_moon_date = ephem.next_full_moon(observer.date)

    next_last_quarter_date = ephem.next_last_quarter_moon(observer.date)

    if observer.date == next_new_moon_date:
        return "New Moon"
    elif observer.date == next_first_quarter_date:
        return "First Quarter"
    elif observer.date == next_last_quarter_date:
        return "Third Quarter"
    elif observer.date == next_full_moon_date:
        return "Full Moon"
    elif observer.date < next_full_moon_date and observer.date < next_new_moon_date:
        if illumination < 50:
            return "Waxing Crescent"
        elif illumination > 50:
            return "Waxing Gibbous"
    elif observer.date > next_full_moon_date and observer.date > next_new_moon_date:
        if illumination < 50:
            return "Waning Crescent"
        elif illumination > 50:
            return "Waning Gibbous"

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
    print("Current moon phase:", phase_name)

    observer = ephem.Observer()
    observer.date = ephem.now()
    moon = ephem.Moon(observer)
    moon.compute()

    illumination_percentage = int(moon.moon_phase * 100)
    message = f"Tonight's phase is a {phase_name}! The moon's illumination is {illumination_percentage}%"
    emoji = resolve_icon(phase_name)

    print("Updating custom status...")
    update_custom_status(message, emoji)
    print("Custom status updated.")

def main():
    global iteration_count
    perform_initial_update()

    while True:
        now = datetime.now() - timedelta(hours=6)  # Convert to CST

        if now.minute == 0:
            print("Checking for moon phase update...")

            phase_name = get_moon_phase()
            print("Current moon phase:", phase_name)

            observer = ephem.Observer()
            observer.date = ephem.now()
            moon = ephem.Moon(observer)
            moon.compute()

            illumination_percentage = int(moon.moon_phase * 100)
            message = f"Tonight's phase is a {phase_name}! The moon's illumination is {illumination_percentage}%"
            emoji = resolve_icon(phase_name)

            print("Updating custom status...")
            update_custom_status(message, emoji)
            print("Custom status updated! Waiting an hour to change status...")

            time.sleep(3600)

            iteration_count = 1
        else:
            print(f"(Iteration {iteration_count}) Not the beginning of the hour. Checking again in a minute...")
            time.sleep(60)

        iteration_count += 1

if __name__ == "__main__":
    main()