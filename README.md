# Discord Music Bot 🎶
A feature-rich Discord bot built with Python to manage music playback, designed to enhance the user experience on Discord servers. This bot supports music queue management, playback controls, and integrates YouTube as a music source.

## Features ✨
### Music Queue Management
Add songs to a queue for continuous playback.
Supports pause, resume, skip, and stop commands.
### YouTube Integration
Play music directly from YouTube using yt-dlp.
Users can search and queue songs by simply providing song names or links.
### Concurrency and Smooth Playback
Ensures smooth audio playback using Python’s asyncio library.
Handles multiple user requests asynchronously without blocking the bot.

## Usage 🛠️
* !play <song_name_or_url> - Adds a song to the queue and starts playback.
* !pause - Pauses the current song.
* !resume - Resumes the paused song.
* !skip - Skips the current song and plays the next in the queue.
* !list_queue - list all of the songs in the queue
* !clear - clear all songs in the list
* !disconnect
## Requirements 📋
* Python 3.8+
* discord.py
* yt-dlp
* Install all dependencies using "pip install -r requirements.txt"

## License 📜
This project is licensed under the MIT License.
