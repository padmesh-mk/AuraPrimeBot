import discord
from discord.ext import commands
from discord import app_commands
import datetime
import platform
import psutil

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.launch_time = datetime.datetime.utcnow()
        self.created_on = datetime.datetime(2024, 12, 12)

    def get_uptime(self):
        delta = datetime.datetime.utcnow() - self.launch_time
        return str(delta).split('.')[0]  # Trim microseconds

    def get_memory_usage(self):
        mem = psutil.Process().memory_info().rss / 1024 / 1024
        return f"{mem:.2f} MB"

    def build_embed(self):
        total_guilds = len(self.bot.guilds)
        total_users = sum(g.member_count or 0 for g in self.bot.guilds)
        latency = round(self.bot.latency * 1000)

        embed = discord.Embed(
            title="<a:ap_bot:1382718727568756857> AuraPrime Bot Info",
            description=(
                "AuraPrime is your all-in-one utility and moderation bot built for clean server management, advanced features, and reliable tools.\n\n"
                "<a:ap_arroworrange:1382746363208667146> Use `a!help` or `/help` to explore commands and get started!"
            ),
            color=discord.Color.orange(),
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(
            name="✨ Key Features",
            value=(
                "`welcomer`, `afk`, `booster`, `userinfo`, `serverinfo`, `minigames`, `moderation`, and more!\n"
                "<a:ap_arroworrange:1382746363208667146> Easy-to-use commands • Fast responses • Constant updates"
            ),
            inline=False
        )

        embed.add_field(name="<:ap_forward:1382775383371419790> Ping", value=f"`{latency} ms`", inline=True)
        embed.add_field(name="<a:ap_uptime:1382717912120430702> Uptime", value=f"`{self.get_uptime()}`", inline=True)
        embed.add_field(name="<:ap_ram:1382719771782549655> Memory", value=f"`{self.get_memory_usage()}`", inline=True)

        embed.add_field(name="<:ap_server:1382719087221674115> Servers", value=f"`{total_guilds}`", inline=True)
        embed.add_field(name="<:ap_users:1382719320072650772> Users", value=f"`{total_users}`", inline=True)
        embed.add_field(name="<:ap_date:1382718456000024631> Created On", value=f"`{self.created_on.strftime('%d %B %Y')}`", inline=True)

        embed.add_field(
            name="<:ap_developer:1382719599283408916> Developer",
            value="<@941902212303556618>",
            inline=True
        )

        embed.set_footer(text="Thanks for choosing AuraPrime!")

        return embed

    def get_view(self):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Invite AuraPrime", url="https://discord.com/oauth2/authorize?client_id=1316827072655523911"))
        view.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/EUfPFvySjw"))
        view.add_item(discord.ui.Button(label="Top.gg Profile", url="https://top.gg/bot/1316827072655523911?s=054eb029926d6"))
        view.add_item(discord.ui.Button(label="Terms of Service", url="https://www.termsfeed.com/live/68397c70-4459-4802-b1f1-2b421b33fdbc"))
        view.add_item(discord.ui.Button(label="Privacy Policy", url="https://www.termsfeed.com/live/cb95c680-336f-4b0e-bc6e-43330e4aad7b"))
        return view

    @commands.command(name="botinfo")
    async def botinfo_prefix(self, ctx):
        """Shows info about AuraPrime bot."""
        await ctx.send(embed=self.build_embed(), view=self.get_view())

    @app_commands.command(name="botinfo", description="Shows info about AuraPrime bot.")
    async def botinfo_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.build_embed(), view=self.get_view())

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
