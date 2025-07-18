import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta, timezone
from collections import Counter
import re

def parse_duration(duration_str):
    pattern = r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?"
    match = re.fullmatch(pattern, duration_str.strip().lower())
    if not match:
        raise ValueError("Invalid format. Use like 5m, 1h30m, 2d, etc.")
    days, hours, minutes, seconds = match.groups()
    total_seconds = (
        int(days or 0) * 86400 +
        int(hours or 0) * 3600 +
        int(minutes or 0) * 60 +
        int(seconds or 0)
    )
    return timedelta(seconds=total_seconds)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _check_permissions(self, ctx_or_interaction, member):
        author = ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author
        me = ctx_or_interaction.guild.me

        if member == me:
            return "I can't moderate myself."
        if member == author:
            return "You can't moderate yourself."
        if member.top_role >= author.top_role and author != ctx_or_interaction.guild.owner:
            return "You can't moderate someone above or equal to you."
        if member.top_role >= me.top_role:
            return "I can't moderate someone with a higher or equal role than mine."
        return None

    async def _respond(self, ctx_or_interaction, content=None, *, embed=None, delete_after=None):
        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(content=content, embed=embed, delete_after=delete_after)
        else:
            await ctx_or_interaction.response.send_message(content=content, embed=embed, ephemeral=True)

    # ---------------- KICK ----------------
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await self._kick(ctx, member, reason)

    @app_commands.command(name="kick", description="Kick a user")
    @app_commands.describe(member="Member to kick", reason="Reason")
    async def slash_kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await self._kick(interaction, member, reason)

    async def _kick(self, ctx_or_interaction, member: discord.Member, reason=None):
        check_msg = self._check_permissions(ctx_or_interaction, member)
        if check_msg:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> {check_msg}")
            return
        try:
            await member.kick(reason=reason)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member} has been kicked.\nReason: {reason or 'No reason provided.'}")
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to kick that member.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to kick: {e}")

    # ---------------- BAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await self._ban(ctx, member, reason)

    @app_commands.command(name="ban", description="Ban a user")
    @app_commands.describe(member="Member to ban", reason="Reason")
    async def slash_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await self._ban(interaction, member, reason)

    async def _ban(self, ctx_or_interaction, member: discord.Member, reason=None):
        check_msg = self._check_permissions(ctx_or_interaction, member)
        if check_msg:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> {check_msg}")
            return
        try:
            await member.ban(reason=reason)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member} has been banned.\nReason: {reason or 'No reason provided.'}")
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to ban that member.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to ban: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str):
        banned_users = await ctx.guild.bans()
        user_name, user_discriminator = user.split("#")

        for ban_entry in banned_users:
            banned_user = ban_entry.user
            if banned_user.name == user_name and banned_user.discriminator == user_discriminator:
                await ctx.guild.unban(banned_user)
                await ctx.send(f"<:ap_checkmark:1382760062728273920> Unbanned {banned_user}.")
                return

        await ctx.send("<:ap_crossmark:1382760353904988230> User not found in ban list.")

    # ---------------- TIMEOUT ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason=None):
        await self._timeout(ctx, member, duration, reason)

    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.describe(member="Member to timeout", duration="Duration", reason="Reason")
    async def slash_timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = None):
        await self._timeout(interaction, member, duration, reason)

    async def _timeout(self, ctx_or_interaction, member: discord.Member, duration: str, reason=None):
        check_msg = self._check_permissions(ctx_or_interaction, member)
        if check_msg:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> {check_msg}")
            return
        try:
            delta = parse_duration(duration)
            until = discord.utils.utcnow().replace(tzinfo=timezone.utc) + delta
            await member.edit(timed_out_until=until, reason=reason)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member.mention} has been timed out for **{duration}**.\nReason: {reason or 'No reason provided.'}")
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to timeout that member.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to timeout: {e}")

    # ---------------- UNTIMEOUT ----------------
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member):
        await self._untimeout(ctx, member)

    @app_commands.command(name="untimeout", description="Untimeout a user")
    @app_commands.describe(member="Member to remove timeout from")
    async def slash_untimeout(self, interaction: discord.Interaction, member: discord.Member):
        await self._untimeout(interaction, member)

    async def _untimeout(self, ctx_or_interaction, member: discord.Member):
        try:
            await member.edit(timed_out_until=None)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member} has been un-timed out.")
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to un-timeout that member.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to un-timeout: {e}")

    # ---------------- TEMPBAN ----------------
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: str, *, reason=None):
        await self._tempban(ctx, member, duration, reason)

    @app_commands.command(name="tempban", description="Temporarily ban a user")
    @app_commands.describe(member="Member to ban", duration="e.g. 1h30m", reason="Reason")
    async def slash_tempban(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = None):
        await self._tempban(interaction, member, duration, reason)

    async def _tempban(self, ctx_or_interaction, member: discord.Member, duration: str, reason=None):
        check_msg = self._check_permissions(ctx_or_interaction, member)
        if check_msg:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> {check_msg}")
            return
        try:
            delta = parse_duration(duration)
            unban_time = discord.utils.utcnow().replace(tzinfo=timezone.utc) + delta
            await member.ban(reason=reason)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member.mention} has been temporarily banned for **{duration}**.\nReason: {reason or 'No reason provided.'}")
            await discord.utils.sleep_until(unban_time)
            await ctx_or_interaction.guild.unban(member)
            await self._respond(ctx_or_interaction, f"<:ap_checkmark:1382760062728273920> {member} has been unbanned after temporary ban.")
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to tempban that member.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to tempban: {e}")

    # ---------------- PURGE ----------------
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await self._purge(ctx, amount)

    @app_commands.command(name="purge", description="Deletes a specified number of messages")
    @app_commands.describe(amount="Number of messages to delete")
    async def slash_purge(self, interaction: discord.Interaction, amount: int):
        await self._purge(interaction, amount)

    async def _purge(self, ctx_or_interaction, amount: int):
        try:
            deleted = await ctx_or_interaction.channel.purge(limit=amount + 1)
            counter = Counter(msg.author for msg in deleted)
            embed = discord.Embed(
                title="<:ap_checkmark:1382760062728273920> Messages Deleted",
                description=f"**Total Deleted:** {len(deleted) - 1} messages",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Requested by {ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author}")
            for user, count in counter.items():
                if user != ctx_or_interaction.guild.me:
                    embed.add_field(name=str(user), value=f"{count} messages", inline=False)
            await self._respond(ctx_or_interaction, embed=embed, delete_after=5)
        except discord.Forbidden:
            await self._respond(ctx_or_interaction, "<:ap_crossmark:1382760353904988230> I don’t have permission to purge messages.")
        except Exception as e:
            await self._respond(ctx_or_interaction, f"<:ap_crossmark:1382760353904988230> Failed to purge: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command is None:
            return

        usage = {
            'kick': '`a!kick @user [reason]`',
            'ban': '`a!ban @user [reason]`',
            'tempban': '`a!tempban @user <duration> [reason]`',
            'timeout': '`a!timeout @user <duration> [reason]`',
            'untimeout': '`a!untimeout @user`',
            'unban': '`a!unban <user#0000>`',
            'purge': '`a!purge <number>`'
        }

        if isinstance(error, commands.MissingRequiredArgument):
            cmd = ctx.command.name
            await ctx.send(f"<:ap_crossmark:1382760353904988230> Missing required arguments.\nUsage: {usage.get(cmd, '`Incorrect usage.`')}")

        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:ap_crossmark:1382760353904988230> Invalid argument. Please mention a valid user or value.")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("<:ap_crossmark:1382760353904988230> You don’t have permission to use this command.")

        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.Forbidden):
                await ctx.send("<:ap_crossmark:1382760353904988230> I don’t have permission to perform this action.")
            else:
                await ctx.send(f"<:ap_crossmark:1382760353904988230> Command failed: `{error.original}`")

        elif isinstance(error, commands.CommandNotFound):
            return

        else:
            await ctx.send(f"<:ap_crossmark:1382760353904988230> An unexpected error occurred: `{error}`")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
