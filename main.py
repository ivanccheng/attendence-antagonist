import discord
from discord import client 
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import os
from dotenv import load_dotenv, find_dotenv
import asyncio
import requests
import logging

# Load environment variables from .env file
load_dotenv(find_dotenv())

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
app = Flask(__name__)


def send_msg(payload):
    res = requests.post(WEBHOOK_URL, json = payload)
    return res.text, res.status_code
    
@app.route('/', methods=['GET'])
def health_check():
    return "Hello", 200

@app.route('/event', methods=['POST'])
def handle_event():
    print(request.json)
    t, c = send_msg(dict(request.json))
    return t, c


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # loop.create_task(run_bot())
    # asyncio.set_event_loop(loop)
    app.run(host="0.0.0.0")
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

