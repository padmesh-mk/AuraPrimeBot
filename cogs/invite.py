import discord
from discord.ext import commands

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1316827072655523911"
SUPPORT_SERVER = "https://discord.gg/EUfPFvySjw"

class Invite(commands.Cog):
    """Get invite link of AuraPrime Bot and Support server."""

    def __init__(self, bot):
        self.bot = bot

    # Prefix command
    @commands.command(name="invite")
    async def invite_cmd(self, ctx):
        embed = discord.Embed(
            title="Thank you for choosing AuraPrime!",
            color = discord.Color(0xff7800)
        )
        embed.add_field(name="<:ap_invite:1382717191052328961> Invite AuraPrime", value=f"[Click here]({INVITE_URL})", inline=False)
        embed.add_field(name="<:ap_support:1382716862256910437> Support Server", value=f"[Join here]({SUPPORT_SERVER})", inline=False)
        embed.set_footer(text="We appreciate your support!")
        await ctx.send(embed=embed)

    # Slash command
    @discord.app_commands.command(name="invite", description="Get the bot's invite and support server link.")
    async def invite_slash(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Thank you for choosing AuraPrime!",
            color=discord.Color.blurple()
        )
        embed.add_field(name="<:ap_invite:1382717191052328961> Invite AuraPrime", value=f"[Click here]({INVITE_URL})", inline=False)
        embed.add_field(name="<:ap_support:1382716862256910437> Support Server", value=f"[Join here]({SUPPORT_SERVER})", inline=False)
        embed.set_footer(text="We appreciate your support!")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Invite(bot))
