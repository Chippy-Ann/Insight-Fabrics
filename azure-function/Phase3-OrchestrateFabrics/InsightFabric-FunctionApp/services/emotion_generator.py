import logging
import json
import os
import random
import uuid
import tempfile
import calendar
from datetime import datetime

import pandas as pd
from faker import Faker

fake = Faker()

# -------------------------
# Emotion selection (range-based)
# -------------------------
emotion_ranges = {
    "happy":      range(0, 30),
    "surprised":  range(30, 50),
    "calm":       range(50, 70),
    "neutral":    range(70, 80),
    "sad":        range(80, 85),
    "angry":      range(85, 90),
    "fear":       range(90, 95),
    "disgust":    range(95, 100)
}

def pick_emotion():
    n = random.randint(0, 99)
    for emotion, r in emotion_ranges.items():
        if n in r:
            return emotion
    return "neutral"

# -------------------------
# Emotion sentences
# -------------------------
emotion_sentences = {
    "happy": [
        "Completed the sprint task and feeling happy.",
        "Everything deployed perfectly and I am excited.",
        "Had a smooth deployment and feeling confident.",
        "The team solved a long‑standing issue and it feels amazing.",
        "Had a productive pairing session and it boosted my mood.",
        "The new feature demo impressed everyone and I’m thrilled.",
        "Finally closed a big ticket and I’m feeling great.",
        "The refactor went smoothly and I’m genuinely happy about it.",
        "Got recognition in stand‑up and it made my morning.",
        "Everything clicked today and I feel upbeat."

    ],
    "surprised": [
        "Deployment succeeded and I feel relieved.",
        "Unexpectedly finished early and feeling surprised.",
        "The performance improvement was far better than expected.",
        "A risky change worked on the first try and I’m shocked.",
        "The customer feedback was unexpectedly positive.",
        "A bug I thought was complex turned out to be trivial.",
        "The system handled the load test surprisingly well.",
        "A teammate jumped in to help without me asking and it surprised me.",
        "The deployment pipeline ran faster than usual and caught me off guard."
    ],
    "calm": [
         "Working steadily and feeling calm.",
        "Today's tasks feel manageable and peaceful.",
        "The performance improvement was far better than expected.",
        "A risky change worked on the first try and I’m shocked.",
        "The customer feedback was unexpectedly positive.",
        "A bug I thought was complex turned out to be trivial.",
        "The system handled the load test surprisingly well.",
        "A teammate jumped in to help without me asking and it surprised me.",
        "The deployment pipeline ran faster than usual and caught me off guard."

    ],
    "neutral": [
        "Working through tasks at a steady pace.",
        "Today's work feels routine and manageable.",
        "Just moving through the backlog without much excitement.",
        "A standard day with predictable tasks.",
        "Nothing special happening, just routine work.",
        "Handling maintenance tasks with no strong feelings.",
        "A typical sprint day with steady progress.",
        "Working through tickets at a normal pace.",
        "No major blockers or wins, just an average day"
    ],
    "sad": [
        "Feeling stuck because the code is not debugging properly.",
        "Review comments are too much and I'm overwhelmed.",
        "Feeling down after struggling with the same issue for hours.",
        "The project delays are starting to affect my mood.",
        "A tough conversation in retro left me feeling low.",
        "Feeling discouraged after missing a deadline.",
        "The workload feels heavy today and it’s draining.",
        "A rejected proposal left me feeling disappointed.",
        "Feeling a bit defeated after another failed attempt"
    ],
    "angry": [
        "Build failed and I am frustrated.",
        "Struggling to fix a production issue and feeling stressed.",
        "The flaky tests are driving me up the wall.",
        "A last‑minute requirement change made me furious.",
        "The system crashed again and I’m losing patience.",
        "Repeating the same fix for the third time is infuriating.",
        "A merge conflict wiped out my work and I’m livid.",
        "The tooling slowdown is making me angry.",
        "A miscommunication caused rework and I’m irritated."
    ],
    "fear": [
        "Blocked by a bug and worried about the deadline.",
        "Worried the upcoming release might introduce regressions.",
        "Feeling anxious about the production freeze.",
        "Concerned that the incident might escalate.",
        "Nervous about presenting the findings to leadership.",
        "Afraid the patch won’t hold under real traffic.",
        "Feeling uneasy about the audit results.",
       "Worried that the root cause might be deeper than expected."
    ],
    "disgust": [
        "The messy codebase is making debugging unpleasant.",
        "The outdated architecture feels painful to maintain.",
        "The spaghetti code makes every change unpleasant.",
        "The inconsistent naming conventions make me cringe.",
        "The legacy service is so messy it feels gross to touch.",
        "The hacky workaround from years ago is still haunting us.",
        "The cluttered repo structure is hard to look at.",
        "The duplicated logic everywhere is downright ugly"
    ]
}

departments = ["Engineering", "QA", "DevOps", "Support", "HR", "Finance"]
def generate_record(index: int,year, month, day):

    emotion = pick_emotion()
    text = random.choice(emotion_sentences[emotion])

    if emotion == "neutral":
        score = random.choice([1, 2])
    else:
        score = random.randint(0, 10)

   
    return {
        "id": str(uuid.uuid4()),
        "index": index,
        "emotion": emotion,
        "score": score,
        "text": text,
        "employee_name": fake.name(),    
        "employee_id": fake.random_int(min=1000, max=9999),
        "department": random.choice(departments),
        "created_at": random_time_on_day(year, month, day)
    }
# -------------------------
# Generate full month with ≥ 30 records/day
# -------------------------
def generate_month_records(totalcount):
    now = datetime.utcnow()
    year = now.year
    month = now.month
    last_day = calendar.monthrange(year, month)[1]
    min_per_day=max(30,int(totalcount/last_day ))
    records = []
    index = 0

    for day in range(1, last_day + 1):
        records_for_day  = min_per_day + random.randint(0, 10)  # optional extra randomness
        for _ in range(records_for_day ):
            records.append(generate_record(index, year, month, day))
            index += 1

    return records

# -------------------------
# Random timestamp for a specific day
# -------------------------
def random_time_on_day(year, month, day):
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime(year, month, day, hour, minute, second).isoformat() + "Z"

