from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv, find_dotenv
import requests
import logging
from collections import defaultdict
from datetime import datetime

# Load environment variables from .env file
load_dotenv(find_dotenv())

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
app = Flask(__name__)


def create_messages(msg_array):
    grouped_data = defaultdict(list)
    msg_array = list(map(lambda x: dict(x), msg_array))
    msg_array = list(map(lambda x: grouped_data[x['person']].append(x), msg_array))


    '''
    returns a dict (k,v)
    where k is the person and v is a list of all changes 
    '''
    return grouped_data


# def format_message(msg):

def format_field(data):
    now = datetime.now().strftime('%Y-%m-%d %H:%M') 
    prac_date = datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    return [
        {
        "name": "Practice Changed",
        "value": "",
        "inline": True
        },
        {
        "name": f"{now}",
        "value": "",
        "inline": True
        },
        {
        "name": "Time until Practice",
        "value": "",
        "inline": True
        },
        {
        "name": "",
        "value": ""
        }]

###
{'Test User': [{'sheetName': 'Fall Attendance', 'cell': 'AG11', 'newValue': '', 'bg': '#f4cccc', 'type_change': 'EDIT', 'type': '6:00pm-7:30pm \nWarrior Zone', 'practice_date': '2024-10-02T04:00:00.000Z', 'date_changed': '09-27T09:23Z', 'person': 'Test User'}]}
###
def format_message(m_entry):
    print("sdklfgjdfkl")
    person = m_entry[0]
    data = m_entry[1]
    
    [{} for d in data]
    
    payload = {
        "username": "KIMMER ANGY",
        "avatar_url": "https://cdn.discordapp.com/attachments/1076630577035354213/1223466186876915772/image.png?ex=6712776d&is=671125ed&hm=0e87a380be66b8de4e277ef2e10d8585cbb4609157aafed437dffdc9cd6d91b6&",
        "content": "Text message. Up to 2000 characters.",
        "embeds": [
            {
                "author": {
                    "name": f"{person}",
                    "url": "https://www.reddit.com/r/cats/",
                    "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
                },
                # "title": f"{person} made changes",
                # "url": "https://google.com/",
                # "description": "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`",
                # "color": 15258703,
                "fields": [
                    {
                    "name": "Practice Changed",
                    "value": "",
                    "inline": True
                    },
                    {
                    "name": "Date Changed",
                    "value": "",
                    "inline": True
                    },
                    {
                    "name": "Time until Practice",
                    "value": "",
                    "inline": True
                    },
                    {
                    "name": "",
                    "value": ""
                    },

                ],
                "thumbnail": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/4-Nature-Wallpapers-2014-1_ukaavUI.jpg"
                },
                "image": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/A_picture_from_China_every_day_108.jpg"
                },
                "footer": {
                    "text": "Woah! So cool! :smirk:",
                    "icon_url": "https://i.imgur.com/fKL31aD.jpg"
                }
            }
        ]
    }
    return payload

def send_payload(p):
    res = requests.post(WEBHOOK_URL, json = p)

def send_msg(payload):
    payload = {"content":str(payload)}
    res = requests.post(WEBHOOK_URL, json = payload)
    return res.text, res.status_code
    
@app.route('/', methods=['GET'])
def health_check():
    return "Hello", 200

@app.route('/event', methods=['POST'])
def handle_event():
    # print(request.json)
    data = request.json

    message_dict = create_messages(data)
    for k,v in message_dict.items():
        send_payload(format_message((k,v)))

    # send_payload(format_message())
    
    # for d in data:
    #     t, c = send_msg(dict(d))
    return "Success", 204


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # loop.create_task(run_bot())
    # asyncio.set_event_loop(loop)
    app.run(host="0.0.0.0")
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

