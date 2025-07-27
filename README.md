# NSBE Scholarship Bot

A Python Discord bot that scrapes the NSBE scholarship page and returns a Discord embed with pagination of all current scholarships. Use !scholarships to trigger the bot.

## Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/nsbe-scholarship-bot.git
cd nsbe-scholarship-bot


## Create and activate a venv
python3 -m venv nsbe-bot-env
source nsbe-bot-env/bin/activate  # Windows: nsbe-bot-env\Scripts\activate

## Install dependencies
pip install -r requirements.txt

The .env file contains the BOT_TOKEN (acquired by only me) & CHANNEL_ID (the channel the bot is allowed to run in)
