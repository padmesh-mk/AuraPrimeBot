# cogs/version.py
import discord
from discord.ext import commands
from discord import app_commands
import json
import os

VERSION_FILE = "version.json"

class Version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version_info = self.load_version()

    def load_version(self):
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, "r") as f:
                return json.load(f)
        return {
            "version": "Unknown",
            "last_updated": "Unknown",
            "developer": "Unknown",
            "changelog": []
        }

    @app_commands.command(name="version", description="Show the current bot version and recent updates")
    async def version(self, interaction: discord.Interaction):
        data = self.version_info
        embed = discord.Embed(
            title=f"<:ap_support:1382716862256910437> AuraPrime v{data['version']}",
            color=discord.Color.blurple(),
            description=f"Created by **{data['developer']}**\nLast updated: `{data['last_updated']}`"
        )

        if data.get("changelog"):
            embed.add_field(
                name="Recent Changes",
                value="\n".join(data["changelog"][:5]),  # Show top 5 changes
                inline=False
            )

        embed.set_footer(text="Thank you for using AuraPrime")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Version(bot))
