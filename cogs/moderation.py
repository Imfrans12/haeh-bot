import discord
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod Commands ready !")

    @app_commands.command(name="clear", description="Delete a specify amount of message from the channel.")
    @app_commands.checks.has_any_role("Mod")
    async def delete_messages(self, interaction:discord.Interaction, amount:int):
        await interaction.response.defer(ephemeral=True)  
        if amount < 1:
            await interaction.channel.send(f"{interaction.user.mention},Input only number")
            return
        deleted_messages = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"{interaction.user.mention} You delete {len(deleted_messages)} message", ephemeral=True)
    
    @app_commands.command(name="kick", description="kicks specify user")
    @app_commands.checks.has_any_role("Mod")
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer()
        await interaction.guild.kick(member)
        await interaction.followup.send(f"{interaction.user.mention} kicked {member.mention}")

    
async def setup(bot):
    await bot.add_cog(Mod(bot))