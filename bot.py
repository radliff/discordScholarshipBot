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
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        scholarships = []
        for link in soup.find_all("a"):
            text = link.get_text(strip=True)
            href = link.get("href")
            if href and ("scholarship" in href.lower() or "scholarship" in text.lower()):
                scholarships.append((text, href))
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
