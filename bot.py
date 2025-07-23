import requests
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID"))
intents = discord.Intents.default()
# so scholarship bot can read ! commands
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def fetch_scholarship_data():
    url = "https://nsbe.org/scholarships/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    scholarships = []
    cards = soup.select("div.search-results-wrapper__result-card")

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

@bot.event
async def on_ready():
    print("Loaded token prefix:", TOKEN[:10])
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="scholarships")
async def send_scholarships(ctx):
    scholarships = fetch_scholarship_data()

    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ This command can only be used in the #scholarships channel.")
        return
    
    if not scholarships:
        await ctx.send("❌ No scholarships found at the moment.")
        return
    
    embed = discord.Embed(title="📢 Latest NSBE Scholarships", color=0x1ABC9C)
    for name, url in scholarships[:5]:
        embed.add_field(name=name, value=f"[Apply here]({url})", inline=False)

    await ctx.send(embed=embed)



if __name__ == "__main__":
    
    bot.run(TOKEN)
