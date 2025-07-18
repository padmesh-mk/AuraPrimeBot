import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

class UserInfo(commands.Cog):
    """Displays detailed information about a user."""
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=member.color if member.color.value else discord.Color.blurple(),
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="Username", value=f"{member.name}#{member.discriminator}", inline=True)
        embed.add_field(name="User ID", value=f"`{member.id}`", inline=True)

        embed.add_field(name="Created At", value=discord.utils.format_dt(member.created_at, style='F'), inline=True)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, style='F'), inline=True)

        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Bot?", value="Yes 🤖" if member.bot else "No", inline=True)
        embed.add_field(name="Roles Count", value=f"`{len(member.roles) - 1}`", inline=True)

        return embed

    @commands.hybrid_command(name="userinfo", description="Shows info about a user.")
    @app_commands.describe(member="The member you want info about.")
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = self.create_embed(member)
        await ctx.reply(embed=embed, mention_author=False)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
