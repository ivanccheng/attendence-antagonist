import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import threading
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Create a Flask app
app = Flask(__name__)

# Endpoint to accept HTTP POST requests
@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    if not data or 'channel_id' not in data or 'message' not in data:
        return jsonify({'error': 'Invalid payload'}), 400

    channel_id = int(data['channel_id'])
    message = data['message']

    channel = bot.get_channel(channel_id)
    if channel:
        asyncio.run_coroutine_threadsafe(channel.send(message), bot.loop)
        return jsonify({'status': 'Message sent'}), 200
    else:
        return jsonify({'error': 'Channel not found'}), 404

# Run Flask in a separate thread
def run_flask():
    app.run(port=5000)

# Start Flask server in a new thread
threading.Thread(target=run_flask).start()

# Basic bot command
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

bot.run(DISCORD_TOKEN)
