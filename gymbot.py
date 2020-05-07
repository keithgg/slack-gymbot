import requests
import random
import hashlib
import datetime
import os

exercises = {
    "upper": {
        "Push Ups": [20, "reps", "https://media.giphy.com/media/Kjj5yTgDdiuvC/giphy.gif"],
        "Burpees": [20, "reps", "https://media.giphy.com/media/23hPPMRgPxbNBlPQe3/giphy.gif"],
        "Shoulder Taps": [20, "reps", "https://cdn.shopify.com/s/files/1/2930/0432/files/shoulder_taps_large.gif?v=1540063651"],
        "Inch Worms": [10, "reps", "https://media.giphy.com/media/UTXzXAwUHGx8MDEtPS/giphy.gif"],
        "Bear Crawls": [30, "seconds", "https://media.giphy.com/media/LWBkgGLVvDBJK/giphy.gif"],
        "Tricep Dips": [20, "reps", "https://media.giphy.com/media/13HOBYXe87LjvW/giphy.gif"],
        "Close-Grip Push Ups": [10, "reps", "http://www.shapefit.com/pics/chest-exercises-push-ups-close-hand-position.gif"],
        "Kick Throughs": [20, "reps", "https://raw.githubusercontent.com/alecvn/slack-gymbot/master/kick_through.gif"],
    },
    "legs": {
        "Squats": [20, "reps", "https://media.giphy.com/media/1qfKN8Dt0CRdCRxz9q/giphy.gif"],
        "Lunges": [20, "reps", "https://media.giphy.com/media/l3q2Q3sUEkEyDvfPO/giphy.gif"],
        "High Knees": [30, "seconds", "https://media.giphy.com/media/l0HlNOsSRC0Bts7iU/giphy.gif"],
        "Mountain Climbers": [30, "seconds", "https://media.giphy.com/media/bWYc47O3jSef6/giphy.gif"],
        "Squat Jumps": [20, "reps", "https://media.giphy.com/media/nmuUOAEvrKTLDT3yTn/giphy.gif"],
        "Side Lunges": [20, "reps", "https://media.giphy.com/media/Pj0wnhvHp3AHMM5ILf/giphy.gif"],
        "Reverse Lunges": [20, "reps", "https://media.giphy.com/media/3o6ozoyJ0IlfuEsuXu/giphy.gif"],
    },
    "core": {
        "Sit Ups": [20, "reps", "https://media.giphy.com/media/9EFCRjJF4EqB2/giphy.gif"],
        "Planks": [30, "seconds", "https://media.giphy.com/media/xT8qBff8cRRFf7k2u4/giphy.gif"],
        "Side Planks": [30, "seconds", "https://media.giphy.com/media/3o6gDUTsbepOYTqTRK/giphy.gif"],
        "Supermans": [20, "reps", "https://media.giphy.com/media/PmPRDFY1ENYMo/giphy.gif"],
        "Leg Raises": [20, "reps", "https://media.giphy.com/media/2LtUR24UvCZdC/giphy.gif"],
        "Bicycle Crunches": [20, "reps", "https://media.giphy.com/media/TMNCtgJGJnV8k/giphy.gif"],
    },
}

today_md5 = hashlib.md5(str(datetime.date.today()).encode("utf-8")).hexdigest()
today_md5_str = str(int(today_md5, base=32))
today_md5_str_mid = int(len(today_md5_str) / 2)

# the sort() here is for python 3.5 which doesn't order keys
upper_keys = list(exercises["upper"].keys())
upper_keys.sort()
legs_keys = list(exercises["legs"].keys())
legs_keys.sort()
core_keys = list(exercises["core"].keys())
core_keys.sort()


def get_key(keys, _list):
    for i in _list:
        try:
            key = keys[int(i)]
            break
        except IndexError:
            pass
    return key


upper_key = get_key(upper_keys, today_md5_str[0:])
legs_key = get_key(legs_keys, today_md5_str[::-1])
core_key = get_key(core_keys, today_md5_str[today_md5_str_mid:])

upper_val = exercises["upper"][upper_key]
legs_val = exercises["legs"][legs_key]
core_val = exercises["core"][core_key]

pretext = ""

if datetime.datetime.now().hour == 8:
    pretext += "Good morning sunshine! \n Now "
elif datetime.datetime.now().hour == 10:
    pretext += "Just before you have that cookie... "
elif datetime.datetime.now().hour == 12:
    pretext += "Lunch is going to taste so much better if you "
elif datetime.datetime.now().hour == 13:
    pretext += "Belly full or barely full, it doesn't change the fact you need to "
elif datetime.datetime.now().hour == 16:
    pretext += "You're almost there big boy... \n Now "
elif datetime.datetime.now().hour == 17:
    pretext += "If you've made it this far, you might as well go all the way... "
else:
    pretext += "Just "

pretext += "drop and give me: \n "

icon_emoji = "aw_yeah"
channel = "#workout"
username = "GymBot"
url = os.environ.get("SLACK_WEBHOOK_URL")

if url == None:
    print("You need to setup an environment variable for the SLACK_WEBHOOK_URL")
else:
    requests.post(
        url,
        json={
            'text': pretext,
            'unfurl_links': False,
            "unfurl_media": False,
            'icon_emoji': icon_emoji,
            'channel': channel,
            'username': username,
            'attachments': [
                {
                    "fallback": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "pretext": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "color":"#FAA71A",
                    "image_url": upper_val[2],
                    "fields": [
                        {
                            "title": "Upper body",
                            "value": "{} ({} {})".format(upper_key, upper_val[0], upper_val[1]),
                            "image_url": upper_val[2],
                            "short": False
                        }
                    ]
                },
                {
                    "fallback": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "pretext": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "color":"#FAA71A",
                    "image_url": legs_val[2],
                    "fields": [
                        {
                            "title": "Legs",
                            "value": "{} ({} {})".format(legs_key, legs_val[0], legs_val[1]),
                            "image_url": legs_val[2],
                            "short": False
                        }
                    ]
                },
                {
                    "fallback": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "pretext": "", # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
                    "color":"#FAA71A",
                    "image_url": core_val[2],
                    "fields": [
                        {
                            "title": "Core",
                            "value": "{} ({} {})".format(core_key, core_val[0], core_val[1]),
                            "image_url": core_val[2],
                            "short": False
                        }
                    ]
                }
            ]
        }
    )
