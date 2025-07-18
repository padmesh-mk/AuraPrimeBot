import discord
from discord.ext import commands
from discord import app_commands
import random
import os
from dotenv import load_dotenv

load_dotenv()
OWNER_ID = int(os.getenv("OWNER_ID", 0))  # Add this to your .env file

class Roast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.roasts = [
            "🚫 {user}, your vibe is a red flag factory.",
            "🪞 {user}, even your reflection rolls its eyes.",
            "📉 {user}, you bring the average IQ down by 40%.",
            "📵 {user}, your opinions are why mute buttons exist.",
            "🧠 {user}, your brain is buffering... permanently.",
            "🧊 {user}, you're about as cool as a microwave.",
            "💀 {user}, you have something on your face — oh wait, that’s just regret.",
            "🪫 {user}, you're running low on relevance.",
            "🧂 {user}, you're saltier than expired chips.",
            "📡 {user}, even Wi-Fi avoids your connection.",
            "🛑 {user}, if cringe was a crime, you’d be doing life.",
            "🗑️ {user}, your content is best left in drafts.",
            "🧻 {user}, you're soft, weak, and easily torn apart.",
            "🧼 {user}, you bring dirt to clean conversations.",
            "🪤 {user}, even traps have more personality.",
            "🥴 {user}, you're the human version of a pop-up ad.",
            "🔕 {user}, your presence is the sound of silence — and not the good kind.",
            "🎯 {user}, always off-target, never on point.",
            "🪦 {user}, your humor belongs in a museum.",
            "🔌 {user}, you're not stupid… just unplugged.",
            "🧃 {user}, you're full of pulp and no juice.",
            "📚 {user}, even autocorrect gives up on you.",
            "🧱 {user}, you’ve got the personality of a brick.",
            "🕳️ {user}, you contribute less than an empty hole.",
            "🥶 {user}, you're colder than your DMs.",
            "🎭 {user}, you’re all drama, no talent.",
            "📦 {user}, you're full of hot air and empty boxes.",
            "📺 {user}, watching paint dry is more thrilling than you.",
            "💤 {user}, even your shadow falls asleep.",
            "🕹️ {user}, you're the lag in every lobby.",
            "💽 {user}, you belong on a floppy disk.",
            "🛠️ {user}, you're a broken tool in the wrong toolbox.",
            "🍞 {user}, even plain bread is spicier than you.",
            "📢 {user}, you’re loud, wrong, and proud.",
            "🦴 {user}, you bring nothing to the table, not even bones.",
            "🎈 {user}, full of air, gone with a pin.",
            "🚪 {user}, the room gets smarter when you leave.",
            "🪑 {user}, you're not even the main character in your own life.",
            "🧬 {user}, evolution gave up halfway.",
            "🪪 {user}, you're the photo ID of failure.",
            "🌪️ {user}, you're a storm of nonsense.",
            "🧊 {user}, you're so cold, even fire won't roast you.",
            "🚽 {user}, you're where good ideas go to die.",
            "💡 {user}, your light bulb’s been out for years.",
            "🧃 {user}, you’re 10% personality, 90% cringe.",
            "🚧 {user}, constant mess, never progress.",
            "🪥 {user}, even plaque avoids you.",
            "🧦 {user}, you’re the lost sock of society.",
            "🎮 {user}, even NPCs avoid you.",
            "🛒 {user}, you’ve got one wheel off the cart.",
            "🧩 {user}, you’re the piece that never fits.",
            "🥄 {user}, even spoons have more edge.",
            "📸 {user}, not even a filter can save you.",
            "📀 {user}, you’re the sequel no one asked for.",
            "🐌 {user}, slow, slimy, and unnecessary.",
            "⏰ {user}, nobody waits for you anymore.",
            "🍂 {user}, you're the crunch under society’s boot.",
            "🔒 {user}, locked in your own mediocrity.",
            "🚿 {user}, even hot water won’t clean that attitude.",
            "📄 {user}, you're the terms and conditions no one reads.",
            "🥫 {user}, you’re past your expiry date.",
            "🎲 {user}, your whole life is a bad roll.",
            "🥕 {user}, a vegetable in every sense.",
            "🪵 {user}, even driftwood has more direction.",
            "📌 {user}, annoying and stuck in the wrong place.",
            "🥤 {user}, all fizz, no flavor.",
            "🧨 {user}, explosive for no reason.",
            "🐠 {user}, all splash, no depth.",
            "🚬 {user}, bad habit energy.",
            "🧯 {user}, always putting out the fun.",
            "🛏️ {user}, you make insomnia worse.",
            "📎 {user}, easily bent and quickly lost.",
            "🔋 {user}, always at 1%.",
            "🔐 {user}, locked in a loop of dumb.",
            "📻 {user}, stuck on static.",
            "📉 {user}, your glow-up got canceled.",
            "🧊 {user}, you chill every room... awkwardly.",
            "🚫 {user}, every decision you make is a cautionary tale.",
            "🍳 {user}, you're all sizzle, no steak.",
            "🥀 {user}, even flowers wilt in your presence.",
            "📮 {user}, outdated and ignored.",
            "🎤 {user}, drop the mic — and don’t pick it back up.",
            "📬 {user}, you deliver disappointment.",
            "🗜️ {user}, tight-minded and rusty.",
            "📠 {user}, you're the fax of the matter: obsolete.",
            "🖨️ {user}, you're always jammed up.",
            "🧽 {user}, soaking up attention with zero use.",
            "🖱️ {user}, always clicking, never making sense.",
            "🎃 {user}, empty-headed and seasonal.",
            "🎳 {user}, easily knocked down.",
            "🧼 {user}, we tried washing away your ego — it got bigger.",
            "🕰️ {user}, you're always late to self-awareness.",
            "🚂 {user}, you're the train wreck people slow down to watch.",
            "📉 {user}, you peaked in the loading screen.",
            "🚘 {user}, no wheels, no direction, just noise.",
            "📟 {user}, outdated tech in a smart world.",
            "🧨 {user}, a walking health hazard — emotionally.",
            "🧊 {user}, if awkward was a temperature, you'd be absolute zero."
        ]

        self.owner_replies = [
            "👑 Roasting Padmesh? Bold move, bug.",
            "🩸 Padmesh runs on salt, code, and revenge.",
            "⚡ Your roast bounced off Padmesh’s sarcasm shield.",
            "🔒 That roast? Denied. Owner-level clearance only.",
            "🕷️ Padmesh patches bugs like you daily.",
            "💀 Brave. Dumb, but brave.",
            "🔥 Padmesh once roasted someone into a 404.",
            "📛 Your ping just got slower. Say thanks to Padmesh.",
            "☠️ You roast Padmesh? Enjoy your infinite loop.",
            "👻 DNS rerouted. Good luck online.",
            "🧙 Padmesh noticed you. You're now a bug report.",
            "🛠️ That roast? Logged and ignored.",
            "⛓️ Root access blocked your roast.",
            "🌪️ Roasting Padmesh? Cool. Bring an umbrella.",
        ]

        self.bot_replies = [
            "🤖 Roasting me? Cute.",
            "⚙️ I run on 1s, 0s, and better comebacks.",
            "💾 Error 404: Roast not found.",
            "🛠️ Try again when you finish Tutorial Mode.",
            "📟 That roast? Rejected by my firewall.",
            "🧠 You just lost a battle to a bot.",
            "☣️ Roast detected. Threat level: harmless.",
            "🧼 Cleaned up your roast with my auto-sanitizer.",
            "🚮 Even my cache dumped that roast.",
            "📎 Clippy wants to help you try again.",
        ]

    @app_commands.command(name="roast", description="Roast yourself or someone else")
    @app_commands.describe(user="User to roast (optional)")
    async def roast_slash(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user

        if target.id == self.bot.user.id:
            return await interaction.response.send_message(random.choice(self.bot_replies), ephemeral=True)

        if OWNER_ID and target.id == OWNER_ID:
            return await interaction.response.send_message(random.choice(self.owner_replies), ephemeral=True)

        roast_line = random.choice(self.roasts).replace("{user}", target.display_name)
        await interaction.response.send_message(roast_line)

    @commands.command(name="roast")
    async def roast_prefix(self, ctx, user: discord.Member = None):
        target = user or ctx.author

        if target.id == self.bot.user.id:
            return await ctx.send(random.choice(self.bot_replies))

        if OWNER_ID and target.id == OWNER_ID:
            return await ctx.send(random.choice(self.owner_replies))

        roast_line = random.choice(self.roasts).replace("{user}", target.display_name)
        await ctx.send(roast_line)

async def setup(bot):
    await bot.add_cog(Roast(bot))
