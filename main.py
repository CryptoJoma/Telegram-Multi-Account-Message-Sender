import time
import pandas as pd
from telethon import TelegramClient
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
CHAT_ID = config.get("chat_id")  # Assuming CHAT_ID is a user ID
if CHAT_ID.isdigit():
    CHAT_ID = int(CHAT_ID)
MSG_TIMER = int(config.get("msg_timer"))
PHONE_NUMBERS = [value for key, value in config.items() if key.startswith('phone')]

# Path to the content folder
content_folder = 'content'

# Read the Excel file
df = pd.read_excel('messages.xlsx')

# Function to send a message using a specific client
async def send_message(client, chat_id, text, image_filename, video_filename):
    await client.connect()
    if not await client.is_user_authorized():
        print(f"Client is not authorized. Please authorize it first.")
        await client.disconnect()
        return

    # Resolve chat ID
    try:
        entity = await client.get_entity(chat_id)
        input_entity = await client.get_input_entity(entity)
        print(f"Chat resolved: {input_entity}")
    except ValueError as e:
        print(f"ValueError: {e}")
        await client.disconnect()
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        await client.disconnect()
        return
    
    # Send the text message if available
    if pd.notna(text):
        await client.send_message(input_entity, str(text))
        print(f"Message sent using {client.session.filename}.")
    
    # Send the image if available
    if pd.notna(image_filename):
        image_path = os.path.join(content_folder, image_filename)
        if os.path.exists(image_path):
            await client.send_file(input_entity, image_path, caption=text)
            print(f"Message sent with image: {image_filename}.")
        else:
            print(f"Image file {image_filename} not found.")

    # Send the video if available
    if pd.notna(video_filename):
        video_path = os.path.join(content_folder, video_filename)
        if os.path.exists(video_path):
            await client.send_file(input_entity, video_path, caption=text)
            print(f"Message sent with video: {video_filename}.")
        else:
            print(f"Video file {video_filename} not found.")

    await client.disconnect()

# Iterate over each row in the DataFrame
async def main():
    for index, row in df.iterrows():
        # Wait for the specified timer before sending the next message
        time.sleep(MSG_TIMER)
        text = row['Text']
        image_filename = row['Image']
        video_filename = row['Video']

        print(f"===============")
        # Use a unique session name for each phone number
        api_id = API_IDS[index % len(API_IDS)]
        api_hash = API_HASHES[index % len(API_HASHES)]
        print(f"This message will be sent using: {api_id} and {api_hash}")
        phone = PHONE_NUMBERS[index % len(PHONE_NUMBERS)]
        print(f"Phone Number to use: {phone}")
        print(f"Chat to send message: {CHAT_ID}")
        session_folder = "sessions"  # Use a folder to manage multiple sessions
        session_name = f'session_{phone}'
        session_path = os.path.join(session_folder, session_name)
        client = TelegramClient(session_path, api_id, api_hash)

        # Send the message using the selected client
        await send_message(client, CHAT_ID, text, image_filename, video_filename)

# Run the main function
import asyncio
asyncio.run(main())
print(f"===============")
print("All messages sent successfully.")
