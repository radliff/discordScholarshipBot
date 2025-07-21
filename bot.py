import requests
import os
import discord
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
intents = discord.Intents.default()
client = discord.Client(intents=intents)

def fetch_scholarship_data():
    url = "https://nsbe.org/scholarships/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    scholarships = []
    cards = soup.select("div.search-results-wrapper_result-card")

    for card in cards:
        link_tag = card.select_one("h3 a")
        if not link_tag:
            continue
    
        name = link_tag.get_text(strip=True)
        href = link_tag.get("href")

        if href and href.startswith("/"):
            href = "https://nsbe.org" + href
        if not href.startswith("https://nsbe.org/scholarship/"):
            continue

        scholarships.append((name, href))

    return scholarships

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    scholarships = fetch_scholarship_data()

    if not scholarships:
        await channel.send("No scholarships found right now")
    else:
        await channel.send("📢 **Latest NSBE Scholarships:**")
        for name, url in scholarships[:5]:
            await channel.send(f"🔗 **{name}**\n{url}")
    await client.close()


if __name__ == "__main__":
    client.run(TOKEN)
