# NSBE Scholarship Bot

A Python Discord bot that scrapes the NSBE scholarship page and returns a Discord embed with pagination of all current scholarships. Use `!scholarships` to trigger the bot.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/nsbe-scholarship-bot.git
cd nsbe-scholarship-bot
```

## Create venv

```bash
python3 -m venv nsbe-bot-env
source nsbe-bot-env/bin/activate  # On Windows: nsbe-bot-env\Scripts\activate
```

## Install Dependencies
```pip install -r requirements.txt```

## .env file
in the root directory - in your .env file add
```
TOKEN=your_bot_token_here
ALLOWED_CHANNEL_ID=your_channel_id_here
```
TOKEN is the bot token (only available to the maintainer)

ALLOWED_CHANNEL_ID is the ID of the channel the bot is allowed to run in


## Running the Bot
The bot is ran w/ scholarships in a channel and returns a paginated embed.


