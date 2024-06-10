# Overview

This repository contains a Python script that automates sending messages to a specified Telegram chat using multiple Telegram accounts. The script supports sending text messages, images, and videos. It uses the Telethon library to interact with the Telegram API and reads message data from an Excel file.

## Features

- **Multi-Account Support**: Send messages from multiple Telegram accounts configured via `config.ini`.
- **Message Timing**: Control the interval between sending messages.
- **Rich Media**: Send text messages with optional images and videos.
- **Easy Configuration**: Manage settings in a simple configuration file.

## Prerequisites

- Python 3.6+
- Telethon library
- pandas library
- An Excel file (`messages.xlsx`) containing the messages to be sent

## Excel File Format
The Excel file (messages.xlsx) should have the following columns:

- Text: The text message to be sent
- Image: The filename of the image to be sent (optional)
- Video: The filename of the video to be sent (optional)

## Configuration

Create a `config.ini` file with the following structure:

```ini
[TELEGRAM]
API_ID_1 = your_api_id_1
API_HASH_1 = your_api_hash_1

CHAT_ID = your_chat_id
MSG_TIMER = interval_between_messages_in_seconds

[PHONES]
PHONE_1 = your_phone_number_1
PHONE_2 = your_phone_number_2
```

## Usage
1. Install Dependencies:
```rb
pip install -r requirements.txt
```
2. Run the Script:
```rb
python main.py
```

## How It Works
1. Configuration Reading:
The script reads API IDs, hashes, phone numbers, chat ID, and message timer from the config.ini file.
2. Message Sending:
It reads messages from the messages.xlsx file.
For each message, it selects an appropriate Telegram account based on the configuration.
It sends the message to the specified chat, including any images or videos if provided.
3. Authorization:
The script ensures that each Telegram client is authorized before sending messages. If not authorized, it prompts for necessary codes and passwords.

## How to Use authorize.py
The authorize.py script is used to authorize multiple Telegram clients using the Telethon library. This is necessary to ensure that each client can send messages through the Telegram API.

### Step-by-Step Instructions
1. Run authorize.py Script
The script will prompt you to enter the verification code sent to each phone number. If two-step verification is enabled, it will also prompt for the password.
```rb
python authorize.py
```
2. Authorize Each Account
For each phone number in your config.ini file, the script will:
- Connect to the Telegram API.
- Send a code request to the phone number.
- Prompt you to enter the code received via SMS or Telegram.

## Notes
- Ensure the folder ‘sessions’ exists.
- Ensure that the images and videos specified in the Excel file exist in the "content" folder.
- Adjust the MSG_TIMER in config.ini to control the delay between sending messages.

## Contribution
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
