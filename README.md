# NSBE Scholarship Bot

A Python Discord bot that scrapes the NSBE scholarship page and returns a Discord embed with pagination of all current scholarships. Use `!scholarships` to trigger the bot.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/nsbe-scholarship-bot.git
cd nsbe-scholarship-bot
2. Create and activate a virtual environment
bash
Copy
Edit
python3 -m venv nsbe-bot-env
source nsbe-bot-env/bin/activate  # On Windows: nsbe-bot-env\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Create a .env file
Create a .env file in the root directory with the following:

ini
Copy
Edit
TOKEN=your_bot_token_here
ALLOWED_CHANNEL_ID=your_channel_id_here
TOKEN is the Discord bot token (only available to the bot maintainer).

ALLOWED_CHANNEL_ID is the channel where the bot is allowed to run.

Running the Bot
bash
Copy
Edit
python bot.py
Type !scholarships in the allowed channel to get current listings with pagination.
