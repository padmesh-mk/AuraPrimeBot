import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

class ServerInfo(commands.Cog):
    """View information about your server."""
    def __init__(self, bot):
        self.bot = bot

    async def create_embed(self, guild: discord.Guild) -> discord.Embed:
        text_channels = len([c for c in guild.channels if isinstance(c, discord.TextChannel)])
        voice_channels = len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)])
        categories = len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)])
        bots = len([m for m in guild.members if m.bot])
        humans = guild.member_count - bots

        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            color=discord.Color.blurple(),
            timestamp=datetime.now(timezone.utc)
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        # Ensure owner fetch
        owner = guild.owner or await guild.fetch_owner()
        owner_mention = owner.mention if owner else "Unknown"

        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=f"`{guild.id}`", inline=True)
        embed.add_field(name="Owner", value=owner_mention, inline=True)

        embed.add_field(
            name="Members",
            value=(
                f"<:ap_users:1382719320072650772> Humans: `{humans}`\n"
                f"<a:ap_bot:1382718727568756857> Bots: `{bots}`\n"
                f"<:ap_chart:1384942967642394654> Total: `{guild.member_count}`"
            ),
            inline=False
        )

        embed.add_field(
            name="Channels",
            value=(
                f"<:ap_chat:1384942326065135647> Text: `{text_channels}`\n"
                f"<:ap_voice:1384942449201250405> Voice: `{voice_channels}`\n"
                f"<:ap_category:1384942626272444418> Categories: `{categories}`"
            ),
            inline=True
        )

        embed.add_field(name="Roles", value=f"`{len(guild.roles)}`", inline=True)
        embed.add_field(name="Emojis", value=f"`{len(guild.emojis)}`", inline=True)
        embed.add_field(
            name="Boosts",
            value=f"Level `{guild.premium_tier}` (`{guild.premium_subscription_count}` boosts)",
            inline=True
        )

        embed.add_field(
            name="Created At",
            value=discord.utils.format_dt(guild.created_at, style='F'),
            inline=False
        )

        return embed

    @commands.hybrid_command(name="serverinfo", description="Shows info about the server.")
    async def serverinfo(self, ctx: commands.Context):
        embed = await self.create_embed(ctx.guild)
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
