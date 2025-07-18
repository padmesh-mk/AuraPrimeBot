import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import time

AFK_FILE = 'afk.json'

def load_afk_data():
    if not os.path.exists(AFK_FILE):
        with open(AFK_FILE, 'w') as f:
            json.dump({}, f)
    with open(AFK_FILE, 'r') as f:
        return json.load(f)

def save_afk_data(data):
    with open(AFK_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def format_duration(seconds):
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if mins: parts.append(f"{mins}m")
    if secs: parts.append(f"{secs}s")
    return ' '.join(parts)

afk_data = load_afk_data()

class AFK(commands.Cog):
    """Track and manage AFK statuses with reasons, duration, and mention logs."""

    def __init__(self, bot):
        self.bot = bot

    def get_user_data(self, guild_id, user_id):
        return afk_data.get(str(guild_id), {}).get(str(user_id))

    def set_user_afk(self, guild_id, user_id, reason, nick):
        guild_str = str(guild_id)
        user_str = str(user_id)
        if guild_str not in afk_data:
            afk_data[guild_str] = {}
        afk_data[guild_str][user_str] = {
            "reason": reason,
            "nick": nick,
            "pinged_by": [],
            "timestamp": time.time()
        }
        save_afk_data(afk_data)

    def clear_user_afk(self, guild_id, user_id):
        guild_str = str(guild_id)
        user_str = str(user_id)
        data = afk_data.get(guild_str, {}).pop(user_str, None)
        if not afk_data.get(guild_str):
            afk_data.pop(guild_str)
        save_afk_data(afk_data)
        return data

    def add_ping(self, guild_id, user_id, pinged_by_id, message_url):
        user_data = self.get_user_data(guild_id, user_id)
        if user_data:
            user_data["pinged_by"].append((pinged_by_id, message_url))
            save_afk_data(afk_data)

    async def send_afk_embed(self, message, user, data):
        timestamp = data.get("timestamp")
        duration = format_duration(time.time() - timestamp) if timestamp else "Unknown"

        embed = discord.Embed(
            title=f"{user.display_name} is AFK",
            description=f"**Reason:** {data['reason']}\n**Since:** `{duration}` ago",
            color=discord.Color.orange()
        )
        sent = await message.reply(embed=embed, mention_author=True)
        await sent.delete(delay=5)

        msg_url = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        self.add_ping(message.guild.id, user.id, message.author.id, msg_url)

    @commands.hybrid_command(name="afk", description="Set your AFK status with a reason")
    @discord.app_commands.describe(reason="Why are you AFK?")
    async def afk(self, ctx: commands.Context, *, reason: str = "AFK"):
        """Set your AFK status with a reason. Adds '[AFK]' to nickname and tracks pings."""
        member = ctx.author
        guild = ctx.guild

        old_nick = member.nick or member.name
        try:
            await member.edit(nick=f"[AFK] {old_nick}")
        except discord.Forbidden:
            pass

        self.set_user_afk(guild.id, member.id, reason, old_nick)

        embed = discord.Embed(
            title=f"<:ap_time:1382729675616555029> {member.display_name} is now AFK",
            description=f"**Reason:** {reason}",
            color=discord.Color.orange()
        )
        await ctx.reply(embed=embed, mention_author=False)

    @app_commands.command(name="clearafk", description="Force remove a user's AFK status (Admin only)")
    @app_commands.describe(user="User whose AFK status should be cleared")
    async def clearafk(self, interaction: discord.Interaction, user: discord.Member):
        """Admin-only command to remove someone else's AFK status."""
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message(
                "<:ap_crossmark:1382760353904988230> You don't have permission to use this command.",
                ephemeral=True
            )

        data = self.clear_user_afk(interaction.guild.id, user.id)
        if data:
            try:
                await user.edit(nick=data["nick"])
            except discord.Forbidden:
                pass

            await interaction.response.send_message(
                f"<:ap_checkmark:1382760062728273920> Removed AFK status for {user.mention}.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{user.mention} is not currently AFK.", ephemeral=True
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        guild_id = str(message.guild.id)
        user_id = str(message.author.id)

        # Clear AFK status
        if self.get_user_data(guild_id, user_id):
            data = self.clear_user_afk(guild_id, user_id)

            try:
                await message.author.edit(nick=data["nick"])
            except discord.Forbidden:
                pass

            timestamp = data.get("timestamp")
            duration = format_duration(time.time() - timestamp) if timestamp else "Unknown"

            embed = discord.Embed(
                title="<:ap_checkmark:1382760062728273920> You're back!",
                description=f"Your AFK status has been removed.\n**AFK Duration:** `{duration}`",
                color=discord.Color.green()
            )

            if data["pinged_by"]:
                pings = "\n".join(
                    f"• <@{uid}> - [message]({url})"
                    for uid, url in data["pinged_by"]
                )
                embed.add_field(name="People who pinged you:", value=pings, inline=False)

            await message.channel.send(embed=embed)

        # Check mentions or reply
        mentioned_afk_users = set()

        for user in message.mentions:
            data = self.get_user_data(message.guild.id, user.id)
            if data and user.id not in mentioned_afk_users:
                mentioned_afk_users.add(user.id)
                await self.send_afk_embed(message, user, data)

        if message.reference and isinstance(message.reference.resolved, discord.Message):
            replied = message.reference.resolved.author
            data = self.get_user_data(message.guild.id, replied.id)
            if data and replied.id not in mentioned_afk_users:
                await self.send_afk_embed(message, replied, data)

async def setup(bot):
    await bot.add_cog(AFK(bot))
