import requests
import random
import hashlib
import datetime
import os
import collections
import pytz

timezone = pytz.timezone("Africa/Johannesburg")
Exercise = collections.namedtuple("Exercise", ["name", "num_reps", "rep_quantity", "image_url"])
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


def get_exercise_json(title, group, attach_images):
    chosen = random.choice(group)

    return {
        "fallback": "",  # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
        "pretext": "",  # "New open task [Urgent]: <http://url_to_task|Test out Slack message attachments>",
        "color": "#FAA71A",
        "image_url": chosen.image_url if attach_images else "",
        "fields": [
            {
                "title": title,
                "value": "{} ({} {})".format(chosen.name, chosen.num_reps, chosen.rep_quantity),
                "short": False,
            }
        ],
    }


EXERCISES = {
    "upper": [
        Exercise("Push Ups", 20, "reps", "https://media.giphy.com/media/Kjj5yTgDdiuvC/giphy.gif"),
        Exercise("Burpees", 20, "reps", "https://media.giphy.com/media/23hPPMRgPxbNBlPQe3/giphy.gif"),
        Exercise(
            "Shoulder Taps",
            20,
            "reps",
            "https://cdn.shopify.com/s/files/1/2930/0432/files/shoulder_taps_large.gif?v=1540063651",
        ),
        Exercise("Inch Worms", 10, "reps", "https://media.giphy.com/media/UTXzXAwUHGx8MDEtPS/giphy.gif",),
        Exercise("Bear Crawls", 30, "seconds", "https://media.giphy.com/media/LWBkgGLVvDBJK/giphy.gif",),
        Exercise("Tricep Dips", 20, "reps", "https://media.giphy.com/media/13HOBYXe87LjvW/giphy.gif",),
        Exercise(
            "Close-Grip Push Ups",
            10,
            "reps",
            "http://www.shapefit.com/pics/chest-exercises-push-ups-close-hand-position.gif",
        ),
        Exercise(
            "Kick Throughs",
            20,
            "reps",
            "https://raw.githubusercontent.com/alecvn/slack-gymbot/master/kick_through.gif",
        ),
    ],
    "legs": [
        Exercise("Squats", 20, "reps", "https://media.giphy.com/media/1qfKN8Dt0CRdCRxz9q/giphy.gif",),
        Exercise("Lunges", 20, "reps", "https://media.giphy.com/media/l3q2Q3sUEkEyDvfPO/giphy.gif",),
        Exercise("High Knees", 30, "seconds", "https://media.giphy.com/media/l0HlNOsSRC0Bts7iU/giphy.gif",),
        Exercise("Mountain Climbers", 30, "seconds", "https://media.giphy.com/media/bWYc47O3jSef6/giphy.gif",),
        Exercise("Squat Jumps", 20, "reps", "https://media.giphy.com/media/nmuUOAEvrKTLDT3yTn/giphy.gif",),
        Exercise("Side Lunges", 20, "reps", "https://media.giphy.com/media/Pj0wnhvHp3AHMM5ILf/giphy.gif",),
        Exercise("Reverse Lunges", 20, "reps", "https://media.giphy.com/media/3o6ozoyJ0IlfuEsuXu/giphy.gif",),
    ],
    "core": [
        Exercise("Sit Ups", 20, "reps", "https://media.giphy.com/media/9EFCRjJF4EqB2/giphy.gif",),
        Exercise("Planks", 30, "seconds", "https://media.giphy.com/media/xT8qBff8cRRFf7k2u4/giphy.gif",),
        Exercise("Side Planks", 30, "seconds", "https://media.giphy.com/media/3o6gDUTsbepOYTqTRK/giphy.gif",),
        Exercise("Supermans", 20, "reps", "https://media.giphy.com/media/PmPRDFY1ENYMo/giphy.gif",),
        Exercise("Leg Raises", 20, "reps", "https://media.giphy.com/media/2LtUR24UvCZdC/giphy.gif",),
        Exercise("Bicycle Crunches", 20, "reps", "https://media.giphy.com/media/TMNCtgJGJnV8k/giphy.gif",),
    ],
}


def send_exercise_message():
    if not WEBHOOK_URL:
        raise ValueError("Add the SLACK_WEBHOOK_URL environment var plox")

    now = datetime.datetime.now(tz=timezone)

    today = now.date()
    seed = hashlib.md5(str(today).encode("utf8"))
    random.seed(seed)

    start_hour = 9
    end_hour = 17
    current_hour = now.hour
    attach_images = current_hour == start_hour

    pretexts = {
        start_hour: "Good morning sunshine! \n Now ",
        10: "Just before you have that cookie... ",
        12: "Lunch is going to taste so much better if you ",
        13: "Belly full or barely full, it doesn't change the fact you need to ",
        16: "You're almost there big boy... \n Now ",
        end_hour: "If you've made it this far, you might as well go all the way... ",
    }

    start_pretext = pretexts.get(current_hour, "Just ")
    pretext = f"{start_pretext} drop and give me: \n "

    icon_emoji = "aw_yeah"
    channel = "#gymbot"
    username = "GymBot"

    requests.post(
        WEBHOOK_URL,
        json={
            "text": pretext,
            "unfurl_links": "false",
            "icon_emoji": icon_emoji,
            "channel": channel,
            "username": username,
            "attachments": [
                get_exercise_json("Upper Body", EXERCISES["upper"], attach_images),
                get_exercise_json("Legs", EXERCISES["legs"], attach_images),
                get_exercise_json("Core", EXERCISES["core"], attach_images),
            ],
        },
    )


if __name__ == "__main__":
    send_exercise_message()
