import discord
import requests
from discord import app_commands
from discord.ext import commands
API_URL_UD = "https://api.urbandictionary.com/v0/"
API_URL_RD = "https://api.urbandictionary.com/v0/random"

def random_dict():
    rd_response = requests.get(f"{API_URL_RD}")
    if rd_response.ok:
        rd_list = rd_response.json()
        if rd_list['list']:
            return rd_list['list'][0]
    return None

def search_dict(term):
    ud_response = requests.get(f"{API_URL_UD}define?term={term}")

    if ud_response.ok:
        ud_list = ud_response.json()
        if ud_list['list']:
            return ud_list['list'][0]
    return None

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online !")

    @app_commands.command(name="dictr", description="Random word")
    async def dictr(self,interaction: discord.Interaction):
        dictr = random_dict()
        cap_word = dictr['word'].capitalize()
        clean_definition = dictr['definition'].translate(str.maketrans('','','[]'))
        rd_response = f"{cap_word} are {clean_definition}\n"
        await interaction.response.send_message(rd_response)
    
    @app_commands.command(name="dict",description="Search meaning based on term")
    async def dict(self, interaction: discord.Interaction, word:str):
        dict = search_dict(word)
        if dict:
            cap_word = dict['word'].capitalize()
            clean_definition = dict['definition'].translate(str.maketrans('','','[]'))
            ud_response = f"{cap_word} are {clean_definition}\n"
            await interaction.response.send_message(ud_response)
        else:
            result = word
            await interaction.response.send_message(f"{result} is not found")