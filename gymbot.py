import requests
import random
import hashlib
import datetime
import os
import collections
import pytz
import json

timezone = pytz.timezone("Africa/Johannesburg")
Exercise = collections.namedtuple("Exercise", ["name", "num_reps", "rep_quantity", "image_url"])
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
CHANNEL_NAME = os.environ.get("CHANNEL_NAME", "gymbot")
USERNAME = os.environ.get("USERNAME", "Gymbot")


def get_message(exercise):
    if exercise.rep_quantity == "reps":
        return f"{exercise.num_reps} {exercise.name}"
    else:
        return f"{exercise.num_reps} {exercise.rep_quantity} of {exercise.name}"


def get_image_json(title, group, attach_images):
    chosen = random.choice(group)
    text = get_message(chosen)

    return {
        "type": "image",
        "image_url": chosen.image_url,
        "alt_text": f"{title}: {text}",
        "title": {"type": "plain_text", "text": f"{title}: {text}"},
    }


def get_text_json(title, group, attach_images):
    chosen = random.choice(group)
    text = get_message(chosen)

    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


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
    random.seed(str(today))

    start_hour = 9
    end_hour = 17
    current_hour = now.hour
    attach_images = current_hour == start_hour

    pretexts = {
        start_hour: "*Good morning sunshine! *\n Now",
        10: "*Just before you have that cookie...*",
        12: "*Lunch is going to taste so much better if you *",
        13: "*Belly full or barely full, it doesn't change the fact you need to *",
        16: "*You're almost there big boy... *\n Now",
        end_hour: "*If you've made it this far, you might as well go all the way...*",
    }

    start_pretext = pretexts.get(current_hour, "Just")
    pretext = f"{start_pretext} drop and give me: \n "

    if current_hour == start_hour:
        get_block = get_image_json
    else:
        get_block = get_text_json

    json_request = {
        "channel": CHANNEL_NAME,
        "username": USERNAME,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": pretext}},
            get_block("Upper Body", EXERCISES["upper"], attach_images),
            get_block("Core", EXERCISES["core"], attach_images),
            get_block("Legs", EXERCISES["legs"], attach_images),
        ],
    }

    return requests.post(WEBHOOK_URL, json=json_request)


if __name__ == "__main__":
    print(send_exercise_message().content)
