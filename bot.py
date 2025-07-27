import requests
import os
import discord
from discord.ext import commands
from discord import Embed, Interaction, ui
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID"))
intents = discord.Intents.default()

# so scholarship bot can read ! commands
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class ScholarshipView(ui.View):
    def __init__(self, scholarships, user_id, chunk_size=5):
        super().__init__(timeout=None)
        self.scholarships = scholarships
        self.user_id = user_id
        self.chunk_size = chunk_size
        self.current_page = 0
    
    def format_page(self):
        start = self.current_page * self.chunk_size
        end = start + self.chunk_size
        embed = Embed(
            title=f"📢 NSBE Scholarships (Page {self.current_page + 1})",
            color=0x1ABC9C
        )
        for name, url in self.scholarships[start:end]:
            embed.add_field(name=name, value=f"[Apply here]({url})", inline=False)
        return embed
    
    # only user who runs !scholarships command can use buttons
    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You can't use this menu. Try '!scholarships' yourself!", ephemeral=True)
            return False
        return True
    
    @ui.button(label="⬅️ Back", style=discord.ButtonStyle.secondary, disabled=True)
    async def back_button(self, interaction: Interaction, button: ui.Button):
        self.current_page -= 1
        self.update_button_states()
        await interaction.response.edit_message(embed=self.format_page(), view=self)
    
    @ui.button(label="➡️ Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: Interaction, button: ui.Button):
        self.current_page += 1
        self.update_button_states()
        await interaction.response.edit_message(embed=self.format_page(), view=self)
    
    def update_button_states(self):
        # do this b/c there might be a remainder - this way we don't have to add an if statement to check
        total_pages = (len(self.scholarships) - 1) // self.chunk_size + 1
        self.back_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= total_pages - 1

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

# this is to test what's being loaded from the .env file
@bot.event
async def on_ready():
    print("Loaded token prefix:", TOKEN[:10])
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="scholarships")
async def send_scholarships(ctx):
    # only posted in #scholarships channel
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ This command can only be used in the #scholarships channel.")
        return

    scholarships = fetch_scholarship_data()
    if not scholarships:
        await ctx.send("❌ No scholarships found.")
        return

    # UI is rendered & shown to user
    view = ScholarshipView(scholarships, user_id=ctx.author.id)
    await ctx.send(embed=view.format_page(), view=view)



if __name__ == "__main__":
    
    bot.run(TOKEN)
