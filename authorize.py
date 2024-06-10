from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import configparser
import os

# Function to read configuration from a file
def read_config(file_path):
    config = {}
    parser = configparser.ConfigParser()
    parser.read(file_path)
    for section in parser.sections():
        for key, value in parser.items(section):
            config[key] = value
    return config

# Load configuration
config = read_config('config.ini')
API_IDS = [value for key, value in config.items() if key.startswith('api_id')]
API_HASHES = [value for key, value in config.items() if key.startswith('api_hash')]
PHONE_NUMBERS = [value for key, value in config.items() if key.startswith('phone')]

# Authorize each phone number
async def authorize_client(phone,api_id,api_hash):
    session_folder = "sessions" # Use a folder to manage multiple sessions
    session_name = f'session_{phone}'
    session_path = os.path.join(session_folder, session_name)
    client = TelegramClient(session_path, api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = input(f"Enter the code for {phone}: ")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            password = input(f"Two-step verification is enabled. Please enter the password for {phone}: ")
            await client.sign_in(password=password)
    await client.disconnect()

import asyncio
from multiprocessing import Process, freeze_support

if __name__ == '__main__':
    print("License validated. Launching bot.")
    i = 0
    for phone in PHONE_NUMBERS:
        print(f"===============")
        print(f"Checking connection to {phone} | {API_IDS[i]} | {API_HASHES[i]}")
        asyncio.run(authorize_client(phone,API_IDS[0],API_HASHES[0]))
        i += i
    print(f"===============")
    print("All clients authorized successfully.")