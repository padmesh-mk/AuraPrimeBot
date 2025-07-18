import discord
from discord.ext import commands

ALLOWED_USER_ID = 941902212303556618  # ✅ Replace with your Discord user ID

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def send_rules(self, ctx):
        """Testing commands (restricted to a owner-only)."""
        if ctx.author.id != ALLOWED_USER_ID:
            return await ctx.reply("🚫 You don't have permission to use this command.", mention_author=False)

        rules_sections = [
            """📜 **Server Rules – AuraPrime Support Server**

Welcome to the official support server for **AuraPrime**!  
This server is dedicated to helping users resolve issues, report bugs, and get assistance with bot-related features.""",

            """**1. Follow Discord’s Terms of Service & Community Guidelines**  
> Any violations will result in action. No harassment, NSFW content, self-bots, or automation abuse.

**2. Respect Staff & Other Members**  
> Be kind and patient. Disrespect won't be tolerated.

**3. No Spam or Flooding**  
> Don’t spam messages or ping unnecessarily.

**4. Use English Only (Unless Otherwise Stated)**  
> Support is English-first unless a language channel says otherwise.

**5. No Self-Promotion or Advertising**  
> No ads in messages or DMs.

**6. Keep It SFW**  
> All usernames, nicknames, messages, and media must be safe for work.

**7. No Mini-Modding**  
> Don't try to moderate others. Report to staff instead.""",

            """🛠 **Support Rules**

**8. Use the Correct Channels for Support**  
> Only ask questions in <#1382423319050981487>.

**9. Don’t Ping Developers**  
> Use support channels, not DMs or random pings.

**10. No Begging or Bribing**  
> Don't offer money or favors for priority help.

**11. No Exploit Talk**  
> Found a bug? Report it in <#1384955740799635477>, don’t abuse it.""",

            """🚨 **Staff Decisions Are Final**  
> If you disagree, open a ticket or DM calmly — don’t argue in public.""",

            """⚠️ **Breaking rules may lead to:**
- Mute / Kick / Ban
- Bot Blacklisting
- Loss of support access

Thanks for keeping this server safe and helpful for everyone!"""
        ]

        for section in rules_sections:
            await ctx.send(section)

async def setup(bot):
    await bot.add_cog(Test(bot))
